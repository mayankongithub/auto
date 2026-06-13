# ⚡ Quick Start Guide

Get your job search automation running in 5 minutes!

## 🚀 Fast Track Setup

### 1. Get API Keys (5 minutes)

**SerpAPI** (for job search):
- Visit: https://serpapi.com/
- Sign up (free)
- Copy your API key from dashboard

**Gmail App Password** (for email):
- Go to: https://myaccount.google.com/security
- Enable 2-Step Verification (if not enabled)
- Click "App passwords" → Select "Mail" → "Other"
- Generate and copy the 16-character password

### 2. Configure (1 minute)

```bash
cd Automation
cp .env.example .env
nano .env  # or use any text editor
```

Fill in:
```env
GLM_API_KEY=25ce45b7393741a0a2e3ecd38cef999f.awjGAbhaLrv1BLzs
SERPAPI_KEY=your_serpapi_key_here
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
```

### 3. Install & Test (2 minutes)

```bash
pip install -r requirements.txt
python test_automation.py
```

### 4. Run Once Manually

```bash
python job_search_automation.py
```

Check your email (mayank0611sharma@gmail.com) for results!

## 🤖 Automate Daily Runs

### Option A: GitHub Actions (Recommended)

```bash
# 1. Create GitHub repo and push code
git init
git add .
git commit -m "Add job search automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main

# 2. Add secrets in GitHub:
# Settings → Secrets → Actions → New repository secret
# Add: GLM_API_KEY, SERPAPI_KEY, SENDER_EMAIL, SENDER_PASSWORD

# 3. Enable Actions in your repo
# Done! Runs daily at 11 PM IST
```

### Option B: Cron (Local)

```bash
./setup_cron.sh
# Follow prompts to add cron job
```

## 📧 What You'll Get

Daily email at 11:00 PM IST with:
- Top job matches (60%+ match score)
- Company names and locations
- Direct application links
- AI-powered matching reasons
- Skills alignment

## 🎯 Tips

✅ Check email daily for fresh job postings  
✅ Apply within 24 hours for best results  
✅ Customize resume for 90%+ matches  
✅ Track applications using saved JSON files  

## ❓ Issues?

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting.

---

**Good luck with your job search! 🎉**
