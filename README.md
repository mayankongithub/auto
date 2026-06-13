# 🎯 Daily Job Search Automation for Mayank Sharma

Automated Python script that searches for relevant software engineering jobs daily, filters them using AI based on your resume, and emails the best matches.

## ✨ Features

- **🔍 Smart Job Search**: Searches across Google Jobs using keywords tailored to your skills
- **🤖 AI-Powered Filtering**: Uses GLM-4 AI to analyze job descriptions and match against your resume
- **📧 Daily Email Reports**: Sends beautifully formatted HTML emails with top job matches
- **⏰ Automated Scheduling**: Runs daily at 11:00 PM IST via GitHub Actions
- **📊 Result Tracking**: Saves job search results as JSON for historical analysis

## 🎓 Tailored For

**Candidate**: Mayank Sharma  
**Email**: mayank0611sharma@gmail.com  
**Target Roles**: Associate Software Engineer, Backend Developer, C++ Developer, Node.js Developer  
**Experience Level**: Fresher/Entry-level (0-1 years)  
**Location**: India  
**Key Skills**: C/C++, JavaScript, Node.js, MongoDB, Distributed Storage Systems

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+** installed
2. **SerpAPI Account** (for Google Jobs search) - [Get free key](https://serpapi.com/)
3. **Gmail Account** with App Password enabled
4. **GitHub Account** (for automated scheduling)

### Local Setup

1. **Clone and navigate to the directory**:
   ```bash
   cd Automation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

4. **Run the script manually**:
   ```bash
   python job_search_automation.py
   ```

### GitHub Actions Setup (Automated Daily Runs)

1. **Push this repository to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Add job search automation"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/job-search-automation.git
   git push -u origin main
   ```

2. **Add GitHub Secrets**:
   - Go to your GitHub repository
   - Navigate to: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`
   - Add the following secrets:
     - `GLM_API_KEY`: Your GLM API key (already provided: `25ce45b7393741a0a2e3ecd38cef999f.awjGAbhaLrv1BLzs`)
     - `SERPAPI_KEY`: Your SerpAPI key from https://serpapi.com/
     - `SENDER_EMAIL`: Your Gmail address
     - `SENDER_PASSWORD`: Your Gmail App Password (see below)

3. **Enable Gmail App Password**:
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Navigate to: `Security` → `2-Step Verification` → `App Passwords`
   - Generate a new app password for "Mail"
   - Use this password as `SENDER_PASSWORD` (not your regular Gmail password)

4. **Enable GitHub Actions**:
   - Go to repository `Actions` tab
   - Enable workflows if prompted
   - The script will now run automatically at 11:00 PM IST (17:30 UTC) daily

5. **Test Manual Run**:
   - Go to `Actions` tab → `Daily Job Search Automation`
   - Click `Run workflow` → `Run workflow`

## 📁 Project Structure

```
Automation/
├── job_search_automation.py    # Main automation script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── README.md                    # This file
├── .github/
│   └── workflows/
│       └── daily_job_search.yml # GitHub Actions workflow
└── job_results_YYYYMMDD.json   # Daily results (auto-generated)
```

## 🔧 Configuration

### Search Keywords
The script searches for these job titles:
- Associate Software Engineer
- Software Developer
- Backend Developer
- C++ Developer
- Node.js Developer
- Distributed Systems

### Candidate Skills (AI Matching)
The GLM AI analyzes jobs against these skills from your resume:
- **Languages**: C, C++, JavaScript
- **Frameworks**: Node.js, Express, React
- **Databases**: MongoDB, MySQL
- **Specializations**: Distributed Storage, System Architecture
- **Experience**: DataDirect Networks (DDN) internship and associate role

### Filtering Criteria
- **Match Score**: Jobs must score ≥60% match
- **Relevance**: Marked as "Entry Level" or "Fresher" suitable
- **Location**: Strictly India
- **AI Analysis**: GLM-4 evaluates job descriptions for skill alignment

## 📧 Email Format

Daily emails include:
- **Job Title**
- **Company Name**
- **Location**
- **Match Score** (AI-calculated percentage)
- **Matching Skills** (highlighted from your resume)
- **AI Analysis** (brief explanation)
- **Direct Application Link**

## 🛠️ Customization

### Change Schedule Time
Edit `.github/workflows/daily_job_search.yml`:
```yaml
schedule:
  - cron: '30 17 * * *'  # 17:30 UTC = 11:00 PM IST
```

### Adjust Match Threshold
Edit `job_search_automation.py`:
```python
filtered_jobs = ai_matcher.filter_jobs(jobs, min_score=60)  # Change 60 to desired score
```

### Add More Keywords
Edit `job_search_automation.py`:
```python
KEYWORDS = [
    "Associate Software Engineer",
    # Add more keywords here
]
```

## 📊 Output Files

Each run generates `job_results_YYYYMMDD.json` containing:
```json
[
  {
    "title": "Backend Developer",
    "company": "Tech Company",
    "location": "Bangalore, India",
    "description": "...",
    "link": "https://...",
    "match_score": 85,
    "relevant": "Yes",
    "matching_skills": ["C++", "Node.js", "MongoDB"],
    "ai_reason": "Strong match for distributed systems and backend development"
  }
]
```

## 🐛 Troubleshooting

### No Email Received
- Verify Gmail App Password is correct
- Check spam/promotions folder
- Ensure `SENDER_EMAIL` and `SENDER_PASSWORD` secrets are set

### No Jobs Found
- Verify `SERPAPI_KEY` is valid and has credits
- Check SerpAPI dashboard for API usage
- Try running manually to see error messages

### GitHub Actions Not Running
- Check if Actions are enabled in repository settings
- Verify cron schedule syntax
- Check Actions tab for error logs

## 📝 License

This is a personal automation script for Mayank Sharma's job search.

## 🙏 Credits

- **AI Matching**: Powered by [GLM-4](https://open.bigmodel.cn/) by Zhipu AI
- **Job Search**: [SerpAPI](https://serpapi.com/) for Google Jobs aggregation
- **Automation**: GitHub Actions

---

**Made with ❤️ for efficient job hunting** 🚀
