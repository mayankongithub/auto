# 📧 Email Setup Guide - Get Job Alerts in Your Inbox!

## ✅ What I Just Fixed:

1. ✅ **Fresher/Entry-Level Filtering** - Now filters out senior positions!
2. ✅ **Code pushed to GitHub** - Ready for email setup

---

## 🎯 How the Filtering Works Now:

### ✅ **INCLUDES** (Fresher Jobs):
- Jobs with: "fresher", "entry level", "junior", "graduate"
- Jobs with: "0-1 year", "0-2 year", "trainee", "intern"
- Jobs with: "recent graduate", "campus"

### ❌ **EXCLUDES** (Senior Jobs):
- Jobs with: "senior", "lead", "manager", "architect"
- Jobs with: "principal", "staff", "sr.", "sr "
- Jobs with: "5+ years", "6+ years", "7+ years", "8+ years"

**Result:** You'll only get jobs suitable for freshers and entry-level candidates!

---

## 📧 SET UP EMAIL DELIVERY (3 Steps)

### Step 1: Generate Gmail App Password (5 minutes)

**Why App Password?**
Gmail doesn't allow regular passwords for apps. You need a special 16-character app password.

**How to Generate:**

1. **Open Google Account Security:**
   - Go to: https://myaccount.google.com/security
   - Log in with your Gmail account

2. **Enable 2-Step Verification** (if not already enabled):
   - Click "2-Step Verification"
   - Follow the setup wizard
   - You'll need your phone to verify

3. **Generate App Password:**
   - Go back to: https://myaccount.google.com/security
   - Scroll down to "2-Step Verification"
   - Click "App passwords"
   - Select:
     - **App:** Mail
     - **Device:** Other (Custom name)
   - Type: "Job Search Bot"
   - Click "Generate"

4. **Copy the Password:**
   - You'll see a 16-character password like: `abcd efgh ijkl mnop`
   - **IMPORTANT:** Copy this now! You won't see it again!
   - Remove spaces if you want: `abcdefghijklmnop`

---

### Step 2: Add Email Secrets to GitHub (2 minutes)

1. **Go to GitHub Secrets:**
   - https://github.com/mayankongithub/auto/settings/secrets/actions

2. **Add First Secret:**
   - Click "New repository secret"
   - Name: `SENDER_EMAIL`
   - Value: `mayank0611sharma@gmail.com`
   - Click "Add secret"

3. **Add Second Secret:**
   - Click "New repository secret" again
   - Name: `SENDER_PASSWORD`
   - Value: `your-16-char-app-password` (paste from Step 1)
   - Click "Add secret"

**You should now have 3 secrets total:**
- ✅ `SERPAPI_KEY`
- ✅ `SENDER_EMAIL`
- ✅ `SENDER_PASSWORD`

---

### Step 3: Test the Email (2 minutes)

1. **Go to Actions:**
   - https://github.com/mayankongithub/auto/actions

2. **Run the Workflow:**
   - Click "Daily Job Search Automation"
   - Click "Run workflow" → "Run workflow"
   - Wait 2-3 minutes

3. **Check Your Email:**
   - Open `mayank0611sharma@gmail.com`
   - Look for email with subject: "Daily Job Alert - X Jobs Found (2026-06-13)"
   - Check spam folder if not in inbox

---

## 📧 What Your Email Will Look Like:

**Subject:** Daily Job Alert - 25 Jobs Found (2026-06-13)

**Content:**
```
🎯 Daily Job Search Results for Mayank Sharma
Date: 2026-06-13
Total Jobs Found: 25

1. Software Engineer - Entry Level
   Company: Tech Solutions Pvt Ltd
   Location: Bangalore, India
   Description: Looking for fresh graduates with C++ and Node.js...
   [Apply Now]

2. Junior Backend Developer
   Company: Startup India
   Location: Pune, India
   Description: Fresher role for backend development...
   [Apply Now]

...and 23 more jobs!
```

---

## 🎯 After Email Setup:

✅ **Daily at 11 PM IST:**
- Automation searches for jobs
- Filters for fresher/entry-level only
- Emails you the results
- Completely automatic!

✅ **In Your Inbox Daily:**
- ~20-40 fresher jobs (filtered from ~50-80 total)
- All from India
- Only entry-level positions
- Direct links to apply

---

## 🔧 Troubleshooting:

### "Invalid credentials" error:
- ❌ Don't use your regular Gmail password
- ✅ Use the 16-character app password
- Make sure you copied it correctly (no spaces)

### No email received:
- Check spam/promotions folder
- Verify both secrets are added correctly
- Check Actions logs for errors

### Still getting senior jobs:
- This is rare after filtering
- The filter excludes jobs with senior keywords
- Report any that slip through (I can improve filter)

---

## 📋 Quick Reference:

| What | Link |
|------|------|
| **Generate App Password** | https://myaccount.google.com/security |
| **Add GitHub Secrets** | https://github.com/mayankongithub/auto/settings/secrets/actions |
| **Test Workflow** | https://github.com/mayankongithub/auto/actions |
| **Your Email** | mayank0611sharma@gmail.com |

---

## 🎉 Once Email is Set Up:

You're 100% done! Here's what happens:

1. **Every day at 11 PM IST** - Automation runs
2. **Searches fresher jobs** - Only entry-level positions
3. **Emails you results** - 20-40 relevant jobs
4. **You apply** - Fresh opportunities daily!

**No more downloading artifacts - just check your email! 📧**

---

**Ready to set up email? Follow Steps 1-3 above! 🚀**
