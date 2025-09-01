from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import PyPDF2
from docx import Document
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import tempfile

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

# load spaCy model for NLP processing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# common skills db with synonyms
SKILLS_DATABASE = {
    "programming": ["python", "java", "javascript", "js", "c++", "c#", "ruby", "php", "swift", "kotlin", "go", "rust", "scala", "typescript", "ts"],
    "web_development": ["html", "css", "react", "react.js", "reactjs", "angular", "vue", "vue.js", "vuejs", "node.js", "nodejs", "express", "django", "flask", "spring", "asp.net", "aspnet", "next.js", "nextjs", "nuxt.js", "nuxtjs"],
    "databases": ["mysql", "postgresql", "postgres", "mongodb", "mongo", "redis", "oracle", "sql server", "sqlserver", "sqlite", "dynamodb", "mariadb", "cassandra"],
    "cloud": ["aws", "amazon web services", "azure", "google cloud", "gcp", "docker", "kubernetes", "k8s", "terraform", "jenkins", "gitlab ci", "gitlabci", "github actions", "githubactions"],
    "data_science": ["pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "sklearn", "tensorflow", "pytorch", "r", "sas", "spark", "hadoop", "jupyter", "notebook"],
    "mobile": ["android", "ios", "react native", "reactnative", "flutter", "xamarin", "swift", "kotlin", "objective-c", "objectivec"],
    "devops": ["git", "jenkins", "docker", "kubernetes", "k8s", "ansible", "terraform", "prometheus", "grafana", "elk", "elasticsearch", "logstash", "kibana"],
    "design": ["photoshop", "illustrator", "figma", "sketch", "adobe xd", "adobexd", "invision", "zeplin", "canva", "xd"],
    "project_management": ["agile", "scrum", "kanban", "jira", "trello", "asana", "monday.com", "mondaycom", "confluence", "slack", "teams"],
    "languages": ["english", "spanish", "french", "german", "chinese", "japanese", "korean", "arabic", "hindi", "portuguese", "italian"],
    "soft_skills": ["leadership", "communication", "teamwork", "problem solving", "problemsolving", "critical thinking", "criticalthinking", "adaptability", "time management", "timemanagement", "creativity", "analytical", "collaboration", "mentoring", "presentation", "negotiation", "project management", "projectmanagement"]
}

# synonym mapping to normalize skill names
SYNONYM_MAPPING = {
    "js": "javascript", "ts": "typescript", "csharp": "c#", "cpp": "c++",
    
    "react.js": "react", "reactjs": "react", "vue.js": "vue", "vuejs": "vue",
    "node.js": "nodejs", "next.js": "nextjs", "nuxt.js": "nuxtjs",
    "asp.net": "aspnet",
    
    "postgres": "postgresql", "mongo": "mongodb", "sqlserver": "sql server",
    "mariadb": "mysql",  # similar enough to group together
    
    "amazon web services": "aws", "gcp": "google cloud", "k8s": "kubernetes",
    "gitlabci": "gitlab ci", "githubactions": "github actions",
    
    "sklearn": "scikit-learn", "jupyter notebook": "jupyter", "notebook": "jupyter",
    
    "reactnative": "react native", "objectivec": "objective-c", "objective-c": "objective-c",
    
    "elk": "elasticsearch",  
    
    "adobexd": "adobe xd", "xd": "adobe xd",
    
    "mondaycom": "monday.com", "projectmanagement": "project management",
    
    "problemsolving": "problem solving", "criticalthinking": "critical thinking",
    "timemanagement": "time management"
}

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    try:
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_text_from_txt(txt_file):
    """Extract text from TXT file"""
    try:
        return txt_file.read().decode('utf-8')
    except Exception as e:
        return f"Error reading TXT: {str(e)}"

def extract_skills(text):
    """Extract skills from text using NLP and pattern matching with normalization and synonyms"""
    # normalize text to lowercase and clean up
    text = text.lower()
    text = re.sub(r'[^\w\s\-\.]', ' ', text)  # remove special characters except hyphens and dots
    text = re.sub(r'\s+', ' ', text).strip()  # normalize whitespace
    
    doc = nlp(text)
    
    entities = [ent.text.lower() for ent in doc.ents]
    nouns = [token.text.lower() for token in doc if token.pos_ == "NOUN" and len(token.text) > 2]
    
    potential_skills = entities + nouns
    
    found_skills = {}
    normalized_text = text
    
    # apply synonym mapping to text
    for synonym, canonical in SYNONYM_MAPPING.items():
        normalized_text = normalized_text.replace(synonym, canonical)
    
    for category, skills in SKILLS_DATABASE.items():
        category_skills = []
        for skill in skills:
            if skill in normalized_text:
                category_skills.append(skill)
            elif re.search(r'\b' + re.escape(skill) + r'\b', normalized_text):
                category_skills.append(skill)
            elif skill.replace(" ", "") in normalized_text.replace(" ", ""):
                category_skills.append(skill)
            elif skill.replace(".", "") in normalized_text.replace(".", ""):
                category_skills.append(skill)
        
        if category_skills:
            unique_skills = []
            for skill in category_skills:
                canonical_skill = skill
                for synonym, canonical in SYNONYM_MAPPING.items():
                    if skill == synonym:
                        canonical_skill = canonical
                        break
                if canonical_skill not in unique_skills:
                    unique_skills.append(canonical_skill)
            
            found_skills[category] = unique_skills
    
    technical_patterns = [
        r'\b[a-z]+\.js\b',  # JavaScript frameworks
        r'\b[a-z]+\.net\b',  # .NET technologies
        r'\b[a-z]+\.io\b',   # Various tools
        r'\b[a-z]+\.com\b',  # Various tools
        r'\b[a-z]+\.ai\b',   # AI tools
        r'\b[a-z]+\.dev\b',  # Development tools
        r'\b[a-z]+\.sh\b',   # Shell scripts
        r'\b[a-z]+\.yml\b',  # YAML files
        r'\b[a-z]+\.yaml\b', # YAML files
    ]
    
    additional_skills = []
    for pattern in technical_patterns:
        matches = re.findall(pattern, normalized_text)
        additional_skills.extend(matches)
    
    if additional_skills:
        found_skills["additional"] = list(set(additional_skills))
    
    return found_skills

def calculate_job_match(resume_skills, job_description):
    """Calculate job match score based on skills with weighted scoring"""
    if not resume_skills or not job_description.strip():
        return 0.0
    
    # normalize JD
    job_description = job_description.lower()
    job_description = re.sub(r'[^\w\s\-\.]', ' ', job_description)
    job_description = re.sub(r'\s+', ' ', job_description).strip()
    
    normalized_job_desc = job_description
    for synonym, canonical in SYNONYM_MAPPING.items():
        normalized_job_desc = normalized_job_desc.replace(synonym, canonical)
    
    # category weights: higher weight for core technical skills
    category_weights = {
        "programming": 1.0,        
        "web_development": 1.0,    
        "databases": 0.9,          
        "cloud": 0.9,              
        "data_science": 0.9,       
        "mobile": 0.8,             
        "devops": 0.8,             
        "design": 0.7,             
        "project_management": 0.6, 
        "languages": 0.5,          
        "soft_skills": 0.4,        
        "additional": 0.7          
    }
    
    # calculate score
    total_score = 0.0
    max_possible_score = 0.0
    matched_skills = []
    
    for category, skills in resume_skills.items():
        if not isinstance(skills, list):
            continue
            
        weight = category_weights.get(category, 0.5)
        category_score = 0.0
        
        for skill in skills:
            if skill in normalized_job_desc:
                category_score += weight
                matched_skills.append(f"{skill} (exact)")
            elif re.search(r'\b' + re.escape(skill) + r'\b', normalized_job_desc):
                category_score += weight
                matched_skills.append(f"{skill} (exact)")
            elif len(skill.split()) > 1 and skill in normalized_job_desc:
                category_score += weight * 0.8
                matched_skills.append(f"{skill} (partial)")
            elif any(word in normalized_job_desc for word in skill.split()):
                category_score += weight * 0.6
                matched_skills.append(f"{skill} (word-level)")
        
        total_score += category_score
        max_possible_score += len(skills) * weight
    
    if max_possible_score > 0:
        skill_score = (total_score / max_possible_score) * 70  
    else:
        skill_score = 0
    
    try:
        all_skills_text = ' '.join([skill for skills_list in resume_skills.values() 
                                   if isinstance(skills_list, list) 
                                   for skill in skills_list])
        
        if all_skills_text and job_description:
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            combined_texts = [all_skills_text, job_description]
            tfidf_matrix = vectorizer.fit_transform(combined_texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            tfidf_score = similarity * 30
        else:
            tfidf_score = 0
    except:
        tfidf_score = 0
    
    final_score = skill_score + tfidf_score
    # bonus points for diverse skill set
    if len(matched_skills) >= 5:
        final_score += 5  # small bonus for excellent skill set
    elif len(matched_skills) >= 3:
        final_score += 2  # small bonus for good skill set
    
    final_score = min(100, final_score)
    
    return round(final_score, 2)

def generate_resume_summary(text, skills):
    """Generate a summary of the resume"""
    lines = text.split('\n')
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    education_keywords = ['education', 'degree', 'bachelor', 'master', 'phd', 'university', 'college']
    education_lines = [line for line in lines if any(keyword in line.lower() for keyword in education_keywords)]
    
    experience_keywords = ['experience', 'work', 'employment', 'job', 'position']
    experience_lines = [line for line in lines if any(keyword in line.lower() for keyword in experience_keywords)]
    
    summary = {
        "total_skills": sum(len(skills_list) for skills_list in skills.values() if isinstance(skills_list, list)),
        "skill_categories": len(skills),
        "contact_info": {
            "emails": emails[:3],  
            "phones": phones[:3]   
        },
        "education_mentions": len(education_lines),
        "experience_mentions": len(experience_lines),
        "text_length": len(text),
        "estimated_pages": max(1, len(text) // 2000)  
    }
    
    return summary

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/scan-resume', methods=['POST'])
def scan_resume():
    """API endpoint to scan resume and extract information"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get job description from form
        job_description = request.form.get('job_description', '')
        
        # Extract text based on file type
        filename = file.filename.lower()
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(file)
        elif filename.endswith('.txt'):
            text = extract_text_from_txt(file)
        else:
            return jsonify({'error': 'Unsupported file format. Please use PDF, DOCX, or TXT.'}), 400
        
        if text.startswith('Error'):
            return jsonify({'error': text}), 400
        
        skills = extract_skills(text)
        match_score = calculate_job_match(skills, job_description)
        summary = generate_resume_summary(text, skills)
        
        response = {
            'success': True,
            'filename': file.filename,
            'skills': skills,
            'job_match_score': match_score,
            'summary': summary,
            'extracted_text_length': len(text)
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    """API endpoint to analyze text directly"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text:
            return jsonify({'error': 'No resume text provided'}), 400
        
        skills = extract_skills(resume_text)
        
        match_score = calculate_job_match(skills, job_description)
        
        summary = generate_resume_summary(resume_text, skills)
        
        response = {
            'success': True,
            'skills': skills,
            'job_match_score': match_score,
            'summary': summary,
            'extracted_text_length': len(resume_text)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
