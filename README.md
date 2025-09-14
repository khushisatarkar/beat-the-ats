# Beat The ATS - AI-Powered Resume Scanner and Analyzer

A modern web application that scans resumes, extracts skills, and provides job matching scores using AI and NLP techniques.

## ✨ Features

- **Multi-format Support**: Upload PDF, DOCX, or TXT resume files
- **Text Input**: Directly paste resume text for analysis
- **Skill Extraction**: AI-powered extraction of technical skills, programming languages, tools, and frameworks
- **Job Matching**: Calculate compatibility scores between resume and job descriptions
- **Smart Analysis**: Uses spaCy NLP and pattern matching for accurate skill detection
- **Modern UI**: Beautiful, responsive web interface with real-time results
- **Comprehensive Results**: Skills breakdown, contact information, education/experience mentions

## 🛠️ How It Works

### Backend (Python/Flask)

- **File Processing**: Extracts text from PDF, DOCX, and TXT files
- **NLP Analysis**: Uses spaCy for named entity recognition and part-of-speech tagging
- **Skill Detection**: Comprehensive skills database with pattern matching
- **Job Matching**: TF-IDF vectorization and cosine similarity for scoring
- **API Endpoints**: RESTful API for file upload and text analysis

### Frontend (HTML/CSS/JavaScript)

- **Modern Design**: Gradient backgrounds, card-based layout, responsive design
- **Dual Input Methods**: File upload and direct text input tabs
- **Real-time Results**: Dynamic display of analysis results
- **Interactive UI**: Hover effects, loading states, and error handling

## 📊 Skills Database

The application recognizes skills across multiple categories:

- **Programming Languages**: Python, Java, JavaScript, C++, C#, Ruby, PHP, Swift, Kotlin, Go, Rust, Scala
- **Web Development**: HTML, CSS, React, Angular, Vue, Node.js, Express, Django, Flask, Spring, ASP.NET
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis, Oracle, SQL Server, SQLite, DynamoDB
- **Cloud & DevOps**: AWS, Azure, Google Cloud, Docker, Kubernetes, Terraform, Jenkins, GitLab CI
- **Data Science**: Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, TensorFlow, PyTorch, R, SAS
- **Mobile Development**: Android, iOS, React Native, Flutter, Xamarin
- **Design Tools**: Photoshop, Illustrator, Figma, Sketch, Adobe XD, InVision, Zeplin
- **Project Management**: Agile, Scrum, Kanban, Jira, Trello, Asana, Monday.com
- **Languages**: English, Spanish, French, German, Chinese, Japanese, Korean, Arabic

## 🔧 API Endpoints

### POST `/scan-resume`

Upload and analyze a resume file.

**Request:**

- `resume`: Resume file (PDF, DOCX, or TXT)
- `job_description`: Job description text (optional)

**Response:**

```json
{
  "success": true,
  "filename": "resume.pdf",
  "skills": {
    "programming": ["python", "javascript"],
    "web_development": ["react", "node.js"]
  },
  "job_match_score": 85.5,
  "summary": {
    "total_skills": 15,
    "skill_categories": 5,
    "contact_info": {...},
    "education_mentions": 2,
    "experience_mentions": 3
  }
}
```

### POST `/analyze-text`

Analyze resume text directly.

**Request:**

```json
{
  "resume_text": "Resume content...",
  "job_description": "Job description..."
}
```

## 📁 Project Structure

```
Resume-Scanner/
├── app.py                # main Flask application
├── requirements.txt       
├── README.md             
├── .gitignore
├── render.yaml           # Render deployment config
└── templates/
    └── index.html        # web interface
```

## 🔍 How Job Matching Works

1. **Skill Extraction**: Parse resume for technical skills and experience using NLP
2. **Keyword Normalization**: Convert all text to lowercase and handle special characters
3. **Synonym Mapping**: Recognize variations like "JS" = "JavaScript", "GCP" = "Google Cloud"
4. **Weighted Scoring**: Apply different weights to skill categories:
   - **70% Technical Skills**: Programming, Web Development, Databases, Cloud, DevOps
   - **30% Soft Skills**: Project Management, Communication, Leadership
5. **Multiple Match Types**: Exact matches, partial matches, and word-level matches
6. **Bonus Points**: Additional points for comprehensive skill sets
7. **Final Score**: Combined weighted score with TF-IDF similarity (0-100%)

## 🎯 Scoring Algorithm Improvements

The application now uses an advanced scoring algorithm that provides more accurate and higher scores:

### **Keyword Normalization**

- Converts all text to lowercase for consistent comparison
- Handles special characters and whitespace variations
- Recognizes different formatting styles

### **Synonym & Alias Mapping**

- **Programming**: JS → JavaScript, TS → TypeScript, C# → C#
- **Web**: React.js → React, Node.js → Nodejs, Vue.js → Vue
- **Databases**: Postgres → PostgreSQL, Mongo → MongoDB
- **Cloud**: GCP → Google Cloud, AWS → Amazon Web Services
- **DevOps**: K8s → Kubernetes, GitLab CI → GitLab CI

### **Weighted Scoring System**

- **Technical Skills (70%)**: Programming, Web Dev, Databases, Cloud, DevOps
- **Soft Skills (30%)**: Project Management, Communication, Leadership
- **Bonus Points**: +5 for 5+ relevant skills, +2 for 3+ skills

### **Multiple Match Types**

- **Exact Matches**: Full skill name recognition
- **Partial Matches**: Compound skills like "machine learning"
- **Word-Level Matches**: Individual word recognition
- **Synonym Matches**: Alias and abbreviation recognition

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🧪 Testing

Test the application with sample resumes:

1. **Sample PDF Resume**: Create a simple PDF with common skills
2. **Sample Job Description**: Use a typical software developer job posting
3. **Verify Results**: Check that skills are correctly extracted and scored

## 🔧 Customization

### Adding New Skills

Edit the `SKILLS_DATABASE` in `app.py`:

```python
SKILLS_DATABASE = {
    "new_category": ["skill1", "skill2", "skill3"],
    # ... existing categories
}
```

### Adding Synonyms

Edit the `SYNONYM_MAPPING` in `app.py`:

```python
SYNONYM_MAPPING = {
    "abbreviation": "full_name",
    "common_name": "technical_name",
    # ... existing mappings
}
```

### Adjusting Scoring Weights

Modify the `category_weights` in the `calculate_job_match` function:

```python
category_weights = {
    "programming": 1.0,        # Core technical skills
    "web_development": 1.0,    # Core technical skills
    "soft_skills": 0.4,        # Soft skills (lower weight)
    # ... adjust weights as needed
}
```

### Modifying Scoring Algorithm

Update the `calculate_job_match` function in `app.py` for different matching logic.

### UI Customization

Modify `templates/index.html` for different styling and layout.

## 🐛 Troubleshooting

### Common Issues

1. **spaCy Model Not Found**

   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **PDF Reading Errors**

   - Ensure PDF is not password-protected
   - Check if PDF contains extractable text (not just images)

3. **Port Already in Use**

   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

4. **Dependencies Installation Issues**

   ```bash
   # Upgrade pip
   python -m pip install --upgrade pip

   # Install with specific versions
   pip install -r requirements.txt --force-reinstall
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

**Happy Resume Scanning!**

## 🙋‍♀️ Developed By Khushi Satarkar 

Connect with me here! (Linkedin: [https://www.linkedin.com/in/khushi-satarkar-039056254/])
