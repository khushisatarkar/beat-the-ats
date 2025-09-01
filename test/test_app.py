#!/usr/bin/env python3
"""
Simple test script for the Resume Scanner application
"""

import requests
import json

def test_text_analysis():
    """Test the text analysis endpoint"""
    print("Testing text analysis endpoint...")
    
    resume_text = """
    John Doe
    Senior Software Engineer
    john.doe@email.com
    
    SKILLS:
    - Programming: Python, JavaScript, Java, TypeScript
    - Web Development: React.js, Node.js, Django, Express, HTML5, CSS3
    - Databases: MySQL, PostgreSQL, MongoDB, Redis
    - Cloud & DevOps: AWS, Docker, Kubernetes, Git, Jenkins, Terraform
    - Data Science: Pandas, NumPy, Scikit-learn
    - Mobile: React Native, Flutter
    - Project Management: Agile, Scrum, Jira
    - Soft Skills: Leadership, Communication, Problem Solving
    
    EXPERIENCE:
    - Senior Full Stack Developer at Tech Corp (2020-2023)
    - Full Stack Developer at Startup Inc (2018-2020)
    
    EDUCATION:
    - Master's in Computer Science from University of Technology
    - Bachelor's in Software Engineering from State University
    """
    
    job_description = """
    We are looking for a Senior Full Stack Developer with experience in:
    - Python, JavaScript, and TypeScript programming
    - React.js, Node.js, and modern web frameworks
    - Database management (MySQL, PostgreSQL, MongoDB)
    - Cloud platforms like AWS and containerization with Docker
    - DevOps practices and CI/CD pipelines
    - Agile development methodologies
    - Leadership and mentoring experience
    """
    
    try:
        response = requests.post(
            'http://localhost:5000/analyze-text',
            json={
                'resume_text': resume_text,
                'job_description': job_description
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("Text analysis successful!")
            print(f"Job Match Score: {data['job_match_score']}%")
            print(f"Total Skills Found: {data['summary']['total_skills']}")
            print(f"Skill Categories: {data['summary']['skill_categories']}")
            
            print("\nExtracted Skills:")
            for category, skills in data['skills'].items():
                print(f"  {category.replace('_', ' ').title()}: {', '.join(skills)}")
            
            print(f"\nResume Summary:")
            print(f"  - Text Length: {data['summary']['text_length']} characters")
            print(f"  - Estimated Pages: {data['summary']['estimated_pages']}")
            print(f"  - Education Mentions: {data['summary']['education_mentions']}")
            print(f"  - Experience Mentions: {data['summary']['experience_mentions']}")
            
            if data['summary']['contact_info']['emails']:
                print(f"  - Contact Emails: {', '.join(data['summary']['contact_info']['emails'])}")
                
        else:
            print(f"Text analysis failed with status {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to the application. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"Error during testing: {str(e)}")

def test_server_status():
    """Test if the server is running"""
    print("Testing server status...")
    
    try:
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            print("Server is running and accessible")
            return True
        else:
            print(f"Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Server is not running or not accessible")
        return False
    except Exception as e:
        print(f"Error checking server status: {str(e)}")
        return False

if __name__ == "__main__":
    print("Resume Scanner Test Suite")
    print("=" * 40)
    
    if test_server_status():
        print("\n" + "=" * 40)
        test_text_analysis()
    else:
        print("\nTo start the server, run: python app.py")
        print("Then run this test script again")
    
    print("\n" + "=" * 40)
    print("Test completed!")
