# 📋 Complete Setup Guide

This guide will walk you through setting up the Daily Job Search Automation from scratch.

## 🎯 Prerequisites Checklist

Before you begin, make sure you have:

- [ ] Python 3.11 or higher installed
- [ ] pip package manager
- [ ] A Gmail account
- [ ] A GitHub account (for automated scheduling)
- [ ] 30 minutes of setup time

## 📝 Step-by-Step Setup

### Step 1: Get SerpAPI Key (Required for Job Search)

1. Visit [https://serpapi.com/](https://serpapi.com/)
2. Click "Register" and create a free account
3. After registration, go to your dashboard
4. Copy your API key (free tier includes 100 searches/month)
5. Save this key - you'll need it in Step 4

**Note**: The free tier is sufficient for daily job searches (30 searches/month for daily runs).

### Step 2: Set Up Gmail App Password (Required for Email)

Since this script sends automated emails, you need an App Password (not your regular Gmail password):

1. Go to [https://myaccount.google.com/](https://myaccount.google.com/)
2. Click **Security** in the left sidebar
3. Under "How you sign in to Google", click **2-Step Verification**
   - If not enabled, enable it first
4. Scroll down and click **App passwords**
5. Select:
   - App: **Mail**
   - Device: **Other (Custom name)** → Enter "Job Search Bot"
6. Click **Generate**
7. Copy the 16-character password (format: xxxx xxxx xxxx xxxx)
8. Save this password - you'll need it in Step 4

### Step 3: Install Python Dependencies

```bash
cd Automation
pip install -r requirements.txt
```

This installs:
- `requests` - For API calls
- `python-dotenv` - For environment variable management

### Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual credentials:
   ```bash
   nano .env  # or use any text editor
   ```

3. Fill in the values:
   ```env
   # GLM API Configuration (already provided)
   GLM_API_KEY=25ce45b7393741a0a2e3ecd38cef999f.awjGAbhaLrv1BLzs

   # SerpAPI Key (from Step 1)
   SERPAPI_KEY=your_serpapi_key_here

   # Gmail Configuration (from Step 2)
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_16_char_app_password
   ```

4. Save and close the file

### Step 5: Test the Setup

Run the test script to verify everything is configured correctly:

```bash
python test_automation.py
```

You should see output showing:
- ✅ Configuration loaded
- ✅ Candidate profile loaded
- ✅ Email format preview
- ✅ All tests passed

### Step 6: Run Manual Test (Optional but Recommended)

Before setting up automation, test the script manually:

```bash
python job_search_automation.py
```

This will:
1. Search for jobs across all keywords
2. Analyze them using GLM AI
3. Send you an email with results
4. Save results to a JSON file

**Expected time**: 5-10 minutes depending on the number of jobs found

### Step 7: Choose Your Automation Method

You have two options for daily automation:

#### **Option A: GitHub Actions (Recommended)**

**Advantages:**
- Free cloud-based automation
- No need to keep your computer running
- Built-in logging and error tracking
- Easy to monitor

**Setup Steps:**

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Job search automation"
   ```

2. **Create GitHub repository**:
   - Go to [https://github.com/new](https://github.com/new)
   - Name: `job-search-automation` (or any name you prefer)
   - Keep it **Private** (recommended for personal automation)
   - Don't initialize with README (we already have one)
   - Click "Create repository"

3. **Push code to GitHub**:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/job-search-automation.git
   git push -u origin main
   ```

4. **Add GitHub Secrets**:
   - Go to your repository on GitHub
   - Click **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret** and add:
     
     | Name | Value |
     |------|-------|
     | `GLM_API_KEY` | `25ce45b7393741a0a2e3ecd38cef999f.awjGAbhaLrv1BLzs` |
     | `SERPAPI_KEY` | Your SerpAPI key from Step 1 |
     | `SENDER_EMAIL` | Your Gmail address |
     | `SENDER_PASSWORD` | Your Gmail app password from Step 2 |

5. **Enable GitHub Actions**:
   - Go to **Actions** tab in your repository
   - Click **"I understand my workflows, go ahead and enable them"**
   - The workflow will now run automatically at 11:00 PM IST daily

6. **Test manual run**:
   - Go to **Actions** tab
   - Click **"Daily Job Search Automation"**
   - Click **"Run workflow"** → **"Run workflow"**
   - Wait for the run to complete (green checkmark)

#### **Option B: Cron Job (For Local Machine)**

**Advantages:**
- Complete control
- No dependency on GitHub
- Works offline

**Disadvantages:**
- Computer must be running at 11:00 PM daily
- No built-in failure notifications

**Setup Steps:**

```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

Follow the prompts to add the cron job to your system.

## 🔍 Verification & Monitoring

### Check Email

After the first run, you should receive an email at `mayank0611sharma@gmail.com` with:
- Subject: "Daily Job Alert - X Matches Found (YYYY-MM-DD)"
- Formatted list of jobs with match scores
- Direct application links

### Check Saved Results

Look for `job_results_YYYYMMDD.json` in the Automation directory:

```bash
cat job_results_$(date +%Y%m%d).json
```

### Monitor GitHub Actions (if using Option A)

1. Go to **Actions** tab in your repository
2. Check the latest workflow run
3. Click on it to see detailed logs
4. Download artifacts to see job results

## 🔧 Customization Options

### Change Schedule Time

**GitHub Actions** (`.github/workflows/daily_job_search.yml`):
```yaml
schedule:
  - cron: '30 17 * * *'  # 17:30 UTC = 11:00 PM IST
```

**Cron** (run `crontab -e`):
```
0 23 * * * /path/to/run_job_search.sh  # 11:00 PM local time
```

### Adjust Match Threshold

Edit `config.py`:
```python
AI_MATCH_THRESHOLD = 60  # Change to 70 for stricter matching, 50 for more results
```

### Add/Remove Keywords

Edit `config.py`:
```python
KEYWORDS = [
    "Associate Software Engineer",
    "Your Custom Keyword Here",  # Add new keywords
    # Remove keywords by deleting or commenting out
]
```

### Change Recipient Email

Edit `config.py`:
```python
RECIPIENT_EMAIL = "different_email@example.com"
```

## 🐛 Troubleshooting

### Issue: No email received

**Solutions:**
1. Check spam/promotions folder
2. Verify `SENDER_EMAIL` and `SENDER_PASSWORD` in `.env`
3. Confirm App Password is correct (16 characters, no spaces)
4. Check Gmail account hasn't blocked the app password

### Issue: "SERPAPI_KEY not set" warning

**Solutions:**
1. Verify `.env` file exists in Automation directory
2. Check `SERPAPI_KEY` is set correctly in `.env`
3. For GitHub Actions, verify the secret is added in repository settings

### Issue: GitHub Actions workflow not running

**Solutions:**
1. Check if Actions are enabled (Settings → Actions → Allow all actions)
2. Verify cron schedule syntax
3. Check workflow file is in `.github/workflows/` directory
4. Manually trigger workflow to test

### Issue: No jobs found

**Solutions:**
1. Check SerpAPI credits (may have exceeded free tier)
2. Try running with different keywords
3. Check if the search location filter is too restrictive

## 📊 Understanding Results

### Match Score

- **90-100**: Excellent match - apply immediately
- **75-89**: Very good match - highly recommended
- **60-74**: Good match - worth considering
- **<60**: Filtered out (not shown in results)

### AI Reasoning

The GLM AI provides explanations like:
- "Strong C++ skills align with job requirements"
- "Distributed systems experience from DDN is valuable"
- "Projects demonstrate relevant full-stack capabilities"

## 🎓 Success Tips

1. **Check emails daily** - Fresh job postings get more applications
2. **Customize your resume** - Tailor for each high-match job (90+)
3. **Apply within 24 hours** - Jobs posted today have fewer applicants
4. **Track applications** - Save the JSON results for reference
5. **Adjust keywords** - Add specific technologies you're interested in

## 📞 Need Help?

- Review the main [README.md](README.md) for feature details
- Run `python test_automation.py` to verify setup
- Check GitHub Actions logs for error messages
- Verify all environment variables are set correctly

---

**Happy job hunting! 🚀**
