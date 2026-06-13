# ✅ Deployment Checklist

Use this checklist to ensure everything is set up correctly.

## 📋 Pre-Deployment

### 1. API Keys & Credentials
- [ ] SerpAPI account created
- [ ] SerpAPI key obtained and tested
- [ ] Gmail 2-Step Verification enabled
- [ ] Gmail App Password generated
- [ ] GLM API key verified (already provided)

### 2. Local Environment
- [ ] Python 3.11+ installed
- [ ] pip package manager working
- [ ] Git installed (for GitHub Actions)
- [ ] Repository cloned/created

### 3. Configuration Files
- [ ] `.env` file created from `.env.example`
- [ ] All environment variables filled in `.env`
- [ ] `GLM_API_KEY` set correctly
- [ ] `SERPAPI_KEY` set correctly
- [ ] `SENDER_EMAIL` set correctly
- [ ] `SENDER_PASSWORD` set correctly

### 4. Dependencies
- [ ] `requirements.txt` present
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] No installation errors

## 🧪 Testing Phase

### 5. Unit Tests
- [ ] Run: `python test_automation.py`
- [ ] All configuration tests pass ✅
- [ ] Candidate summary generates correctly ✅
- [ ] Email format preview displays ✅
- [ ] No errors in output

### 6. Manual Run Test
- [ ] Run: `python job_search_automation.py`
- [ ] Job search starts successfully
- [ ] No API errors (check SerpAPI credits)
- [ ] AI analysis runs (check GLM API)
- [ ] Email sent successfully
- [ ] Check inbox for test email
- [ ] JSON file created: `job_results_YYYYMMDD.json`

### 7. Output Validation
- [ ] Email received in inbox (check spam too)
- [ ] Email formatting looks good (HTML rendered)
- [ ] Job listings present and relevant
- [ ] Match scores displayed correctly
- [ ] Application links clickable
- [ ] JSON file has valid structure

## 🚀 Deployment (Choose One)

### Option A: GitHub Actions Deployment

#### 8. GitHub Repository Setup
- [ ] GitHub repository created
- [ ] Repository is private (recommended)
- [ ] Local git initialized: `git init`
- [ ] Files added: `git add .`
- [ ] Initial commit: `git commit -m "Initial commit"`
- [ ] Remote added: `git remote add origin <URL>`
- [ ] Code pushed: `git push -u origin main`

#### 9. GitHub Secrets Configuration
- [ ] Navigate to: Settings → Secrets → Actions
- [ ] Add secret: `GLM_API_KEY`
- [ ] Add secret: `SERPAPI_KEY`
- [ ] Add secret: `SENDER_EMAIL`
- [ ] Add secret: `SENDER_PASSWORD`
- [ ] All 4 secrets showing in list

#### 10. GitHub Actions Verification
- [ ] Navigate to: Actions tab
- [ ] Workflow file detected: `daily_job_search.yml`
- [ ] Actions enabled (not disabled)
- [ ] Manual trigger test: Run workflow button clicked
- [ ] Workflow run starts successfully
- [ ] Workflow completes without errors (green checkmark)
- [ ] Artifacts downloadable (job results JSON)
- [ ] Email received from workflow run

#### 11. Schedule Verification
- [ ] Cron schedule correct: `30 17 * * *` (11 PM IST)
- [ ] Next scheduled run shows in Actions tab
- [ ] Wait for first scheduled run (or skip to production)

### Option B: Cron Job Deployment

#### 8. Cron Setup
- [ ] Run: `chmod +x setup_cron.sh`
- [ ] Run: `./setup_cron.sh`
- [ ] Script prompts for confirmation
- [ ] Confirm to add cron job
- [ ] Crontab entry added successfully

#### 9. Cron Verification
- [ ] Run: `crontab -l` to view cron jobs
- [ ] Job search entry visible in list
- [ ] Time set correctly (11:00 PM local)
- [ ] Wrapper script path correct

#### 10. Cron Test Run
- [ ] Run wrapper manually: `./run_job_search.sh`
- [ ] Script executes successfully
- [ ] Email received
- [ ] Check `cron_log.txt` for output

## 🎯 Production Readiness

### 12. Documentation Review
- [ ] `README.md` read and understood
- [ ] `QUICK_START.md` reviewed
- [ ] `SETUP_GUIDE.md` bookmarked for reference
- [ ] `PROJECT_OVERVIEW.md` reviewed for technical details

### 13. Monitoring Setup
- [ ] Email filters created (optional, to organize job alerts)
- [ ] Calendar reminder set to check emails daily
- [ ] Tracking spreadsheet prepared (optional)

### 14. First Week Validation
- [ ] Day 1: Email received ✅
- [ ] Day 2: Email received ✅
- [ ] Day 3: Email received ✅
- [ ] Day 4: Email received ✅
- [ ] Day 5: Email received ✅
- [ ] Day 6: Email received ✅
- [ ] Day 7: Email received ✅

### 15. Quality Check (After First Week)
- [ ] Match quality satisfactory (60%+ scores relevant)
- [ ] Sufficient job volume (~10-20 per day)
- [ ] No false positives (irrelevant jobs)
- [ ] Email deliverability good (not in spam)
- [ ] No API rate limit errors

## 🔧 Optimization (Optional)

### 16. Tuning Parameters
- [ ] Adjust `AI_MATCH_THRESHOLD` if needed (default: 60)
- [ ] Add/remove keywords based on results
- [ ] Change location if needed
- [ ] Modify email format preferences

### 17. Advanced Features (If Needed)
- [ ] Add more job search sources
- [ ] Implement duplicate tracking across days
- [ ] Set up Slack/Telegram notifications
- [ ] Create weekly summary reports

## 📊 Maintenance Schedule

### Daily
- [ ] Check email for new job alerts
- [ ] Review match quality
- [ ] Apply to relevant jobs

### Weekly
- [ ] Review SerpAPI usage (100 free/month)
- [ ] Check for any errors in logs
- [ ] Analyze JSON files for trends

### Monthly
- [ ] Update resume profile if skills change
- [ ] Review keyword effectiveness
- [ ] Check API credit usage
- [ ] Archive old JSON files

## 🆘 Troubleshooting Reference

If issues arise, check:
1. **No email**: Verify Gmail App Password, check spam folder
2. **No jobs found**: Check SerpAPI credits, verify keywords
3. **Low match scores**: Adjust threshold, update resume profile
4. **API errors**: Check API keys, verify rate limits
5. **Workflow fails**: Check GitHub Actions logs, verify secrets

## ✅ Final Sign-Off

- [ ] All critical tests passed
- [ ] Automation running successfully
- [ ] Email notifications working
- [ ] Monitoring in place
- [ ] Documentation accessible
- [ ] Ready for production! 🚀

---

**Deployment Date**: ________________  
**Deployed By**: Mayank Sharma  
**Status**: ⬜ In Progress | ⬜ Complete | ⬜ Issues Found  

**Notes**:
_______________________________________________________
_______________________________________________________
_______________________________________________________
