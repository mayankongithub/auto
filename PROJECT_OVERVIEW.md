# 📊 Project Overview - Daily Job Search Automation

## 🎯 Project Summary

An intelligent, AI-powered job search automation system that:
- **Searches** multiple job boards daily using targeted keywords
- **Analyzes** job descriptions using GLM-4 AI against your resume
- **Filters** irrelevant listings to show only high-quality matches
- **Emails** results daily at 11:00 PM IST with actionable insights
- **Saves** historical data for tracking and analysis

## 📁 Project Structure

```
Automation/
├── 📄 Core Scripts
│   ├── job_search_automation.py    # Main automation script (300+ lines)
│   ├── config.py                   # Centralized configuration
│   └── test_automation.py          # Testing suite
│
├── ⚙️ Configuration
│   ├── .env.example                # Environment variables template
│   ├── requirements.txt            # Python dependencies
│   └── .gitignore                  # Git ignore rules
│
├── 🤖 Automation Setup
│   ├── .github/workflows/
│   │   └── daily_job_search.yml    # GitHub Actions workflow
│   └── setup_cron.sh               # Local cron setup script
│
└── 📚 Documentation
    ├── README.md                   # Main documentation
    ├── QUICK_START.md              # 5-minute setup guide
    ├── SETUP_GUIDE.md              # Detailed setup instructions
    └── PROJECT_OVERVIEW.md         # This file
```

## 🔧 Technical Architecture

### Components

1. **JobSearcher Class**
   - Integrates with SerpAPI for Google Jobs search
   - Searches 8 job-related keywords
   - Deduplicates results
   - Rate-limited API calls

2. **AIJobMatcher Class**
   - Uses GLM-4 AI API for intelligent matching
   - Analyzes job descriptions vs. candidate profile
   - Scores jobs 0-100 for relevance
   - Filters out jobs below 60% match threshold

3. **EmailNotifier Class**
   - Formats results into professional HTML emails
   - Includes match scores and reasoning
   - Sends via Gmail SMTP
   - Error handling and logging

4. **Configuration Module**
   - Centralizes all settings
   - Candidate profile data
   - API endpoints and keys
   - Customizable parameters

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| Job Search API | SerpAPI (Google Jobs) |
| AI Matching | GLM-4 by Zhipu AI |
| Email | Gmail SMTP with App Passwords |
| Scheduling | GitHub Actions / Cron |
| Data Storage | JSON files |

## 🎓 Candidate Profile

**Target**: Mayank Sharma  
**Email**: mayank0611sharma@gmail.com  
**Education**: B.E. in Computer Science, Chitkara University (2022-2026)  
**CGPA**: 8.9

### Key Skills
- **Languages**: C, C++, JavaScript
- **Frameworks**: Node.js, Express, React
- **Databases**: MongoDB, MySQL
- **Specialization**: Distributed Storage Systems, System Architecture

### Experience
- Associate Software Engineer @ DataDirect Networks (April 2026 - Present)
- Tech Intern @ DataDirect Networks (April 2025 - March 2026)

### Notable Projects
- Synapse (AI coding assistant)
- VS Code Extension (Redux snippets)
- Summarize It (AI webpage summarizer)

## 🔍 Search Configuration

### Keywords (8 total)
1. Associate Software Engineer
2. Software Developer
3. Backend Developer
4. C++ Developer
5. Node.js Developer
6. Distributed Systems Engineer
7. Software Engineer Fresher
8. Entry Level Developer

### Filters
- **Location**: India (strict)
- **Experience**: Fresher / Entry-level (0-1 years)
- **Job Age**: Today's postings preferred
- **Match Threshold**: ≥60% AI match score

## 📧 Email Output Format

Daily emails include:

```
Subject: Daily Job Alert - X Matches Found (YYYY-MM-DD)

For each job:
├── Job Title
├── Company Name
├── Location
├── Match Score (AI-calculated %)
├── Matching Skills (highlighted)
├── AI Analysis (reasoning)
└── Direct Application Link
```

## 🤖 Automation Options

### Option 1: GitHub Actions (Cloud)
- **Schedule**: Daily at 17:30 UTC (11:00 PM IST)
- **Cost**: Free
- **Uptime**: 99.9%+
- **Logs**: Built-in workflow logs
- **Setup Time**: 10 minutes

### Option 2: Cron Job (Local)
- **Schedule**: Daily at 11:00 PM local time
- **Cost**: Free
- **Uptime**: Requires machine to be running
- **Logs**: Custom log file
- **Setup Time**: 5 minutes

## 📊 Data Flow

```
1. Trigger (11:00 PM IST)
   ↓
2. Search Jobs (SerpAPI)
   - 8 keywords × ~10 jobs each
   - ~80 raw results
   ↓
3. Deduplicate
   - Remove duplicate listings
   - ~50-60 unique jobs
   ↓
4. AI Analysis (GLM-4)
   - Score each job 0-100
   - Extract matching skills
   - Generate reasoning
   ↓
5. Filter (≥60% match)
   - Keep high-quality matches
   - ~10-20 relevant jobs
   ↓
6. Send Email + Save JSON
   - Email to recipient
   - Save to job_results_YYYYMMDD.json
```

## 🔐 Security & Privacy

- ✅ API keys stored in environment variables (not in code)
- ✅ `.env` file excluded from version control
- ✅ GitHub Secrets for sensitive data
- ✅ Gmail App Passwords (not regular passwords)
- ✅ HTTPS for all API communications

## 📈 Expected Results

### Daily Metrics
- **Jobs Searched**: ~80 raw listings
- **After Deduplication**: ~50-60 unique jobs
- **After AI Filtering**: ~10-20 high-quality matches
- **Email Recipients**: 1 (mayank0611sharma@gmail.com)
- **Execution Time**: 5-10 minutes

### Match Score Distribution
- **90-100%**: Excellent matches (apply immediately)
- **75-89%**: Very good matches (highly recommended)
- **60-74%**: Good matches (worth considering)
- **<60%**: Filtered out (not shown)

## 🎯 Use Cases

1. **Daily Job Discovery**: Automated scanning of fresh job postings
2. **Quality Filtering**: AI removes irrelevant jobs (saves time)
3. **Skills Matching**: Highlights why each job is a good fit
4. **Application Tracking**: JSON files for historical analysis
5. **Early Application**: Get notified same day as job posting

## 🔄 Maintenance

### Weekly
- Check email inbox for results
- Review match quality
- Adjust keywords if needed

### Monthly
- Review SerpAPI usage (100 free searches/month)
- Check GitHub Actions minutes (2000 free/month)
- Analyze job trends from saved JSON files

### As Needed
- Update resume profile in `config.py`
- Adjust match threshold (60% default)
- Add/remove search keywords
- Change schedule time

## 📝 Customization Points

All easily configurable in `config.py`:

```python
# Adjust these to customize behavior
AI_MATCH_THRESHOLD = 60          # Strictness (higher = fewer results)
KEYWORDS = [...]                 # Add/remove job titles
LOCATION = "India"               # Change location
MAX_JOBS_PER_KEYWORD = 10        # Increase for more results
RECIPIENT_EMAIL = "..."          # Change recipient
```

## 🚀 Future Enhancements (Optional)

- [ ] Add Indeed API integration
- [ ] LinkedIn job scraping
- [ ] Multiple recipient support
- [ ] Telegram/Slack notifications
- [ ] Weekly summary reports
- [ ] Job application tracking
- [ ] Salary filtering
- [ ] Company rating integration

## 📞 Support & Resources

- **Documentation**: README.md, SETUP_GUIDE.md, QUICK_START.md
- **Testing**: Run `python test_automation.py`
- **Logs**: Check GitHub Actions or `cron_log.txt`
- **API Docs**: 
  - SerpAPI: https://serpapi.com/google-jobs-api
  - GLM-4: https://open.bigmodel.cn/dev/api

---

**Built with ❤️ for efficient job hunting**
