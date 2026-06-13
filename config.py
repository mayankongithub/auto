"""
Configuration file for job search automation
Centralizes all settings and constants
"""

import os
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys and Credentials
GLM_API_KEY = os.getenv("GLM_API_KEY", "25ce45b7393741a0a2e3ecd38cef999f.awjGAbhaLrv1BLzs")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

# Email Configuration
RECIPIENT_EMAIL = "mayank0611sharma@gmail.com"
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")

# Job Search Keywords
KEYWORDS = [
    "Associate Software Engineer",
    "Software Developer",
    "Backend Developer",
    "C++ Developer",
    "Node.js Developer",
    "Distributed Systems Engineer",
    "Software Engineer Fresher",
    "Entry Level Developer"
]

# Location and Experience Filters
LOCATION = "India"
EXPERIENCE_LEVELS = ["Fresher", "Entry Level", "0-1 years", "Graduate"]

# Candidate Profile for AI Matching
CANDIDATE_PROFILE = {
    "name": "Mayank Sharma",
    "email": "mayank0611sharma@gmail.com",
    "phone": "+91-9649356720",
    
    "education": {
        "degree": "Bachelor of Engineering in Computer Science",
        "university": "Chitkara University Institute of Engineering and Technology, Punjab",
        "duration": "2022-2026",
        "cgpa": "8.9"
    },
    
    "experience": [
        {
            "title": "Associate Software Engineer",
            "company": "DataDirect Networks (DDN)",
            "duration": "April 2026 - Present",
            "highlights": [
                "Engineered and optimized distributed storage system architectures",
                "Improved system performance and reliability"
            ]
        },
        {
            "title": "Tech Intern",
            "company": "DataDirect Networks (DDN)",
            "duration": "April 2025 - March 2026",
            "highlights": [
                "Enhanced core product UI",
                "Worked on storage server hardware components",
                "Debugging and performance analysis of distributed systems"
            ]
        }
    ],
    
    "skills": {
        "languages": ["C", "C++", "JavaScript"],
        "frameworks_libraries": ["Node.js", "Express", "React", "TailwindCSS"],
        "databases": ["MongoDB", "MySQL"],
        "tools": ["VS Code", "Git", "GitHub"],
        "specializations": [
            "Distributed Storage Systems",
            "System Architecture",
            "Data Structures & Algorithms",
            "Operating Systems",
            "Database Management Systems"
        ]
    },
    
    "projects": [
        {
            "name": "Synapse",
            "description": "Browser-based AI coding assistant for real-time code analysis, debugging, and execution using Google Gemini",
            "tech_stack": ["Node.js", "Express", "React", "File System Access API", "TailwindCSS"]
        },
        {
            "name": "VS Code Extension",
            "description": "Redux snippet extension with live users",
            "tech_stack": ["JavaScript"]
        },
        {
            "name": "Summarize It",
            "description": "AI-powered browser extension for webpage summaries",
            "tech_stack": ["HTML", "CSS", "JavaScript"]
        }
    ],
    
    "achievements": [
        "700+ questions solved on coding platforms",
        "National Competence And Employability Test (A+)"
    ]
}

# AI Matching Configuration
AI_MATCH_THRESHOLD = 60  # Minimum match score (0-100)
AI_MODEL = "glm-4"
AI_TEMPERATURE = 0.7

# Email Configuration
EMAIL_SUBJECT_TEMPLATE = "Daily Job Alert - {count} Matches Found ({date})"
EMAIL_FROM_NAME = "Job Search Bot"

# Rate Limiting (seconds)
RATE_LIMIT_BETWEEN_SEARCHES = 2
RATE_LIMIT_BETWEEN_AI_CALLS = 1

# API Endpoints
GLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
SERPAPI_URL = "https://serpapi.com/search"

# Output Configuration
RESULTS_FILENAME_TEMPLATE = "job_results_{date}.json"
LOG_FILENAME = "job_search.log"

# Search Limits
MAX_JOBS_PER_KEYWORD = 10
MAX_TOTAL_JOBS = 100

def get_candidate_summary() -> str:
    """Returns a formatted summary of candidate profile for AI prompts"""
    profile = CANDIDATE_PROFILE
    
    summary = f"""
CANDIDATE PROFILE: {profile['name']}
Education: {profile['education']['degree']}, {profile['education']['university']} (CGPA: {profile['education']['cgpa']})
Graduation: 2026

Technical Skills:
- Languages: {', '.join(profile['skills']['languages'])}
- Frameworks: {', '.join(profile['skills']['frameworks_libraries'])}
- Databases: {', '.join(profile['skills']['databases'])}
- Specializations: {', '.join(profile['skills']['specializations'])}

Experience:
- {profile['experience'][0]['title']} at {profile['experience'][0]['company']} ({profile['experience'][0]['duration']})
  * {', '.join(profile['experience'][0]['highlights'])}
- {profile['experience'][1]['title']} at {profile['experience'][1]['company']} ({profile['experience'][1]['duration']})
  * {', '.join(profile['experience'][1]['highlights'])}

Key Projects:
- {profile['projects'][0]['name']}: {profile['projects'][0]['description']}
- {profile['projects'][1]['name']}: {profile['projects'][1]['description']}
- {profile['projects'][2]['name']}: {profile['projects'][2]['description']}

Achievements: {', '.join(profile['achievements'])}
"""
    return summary.strip()
