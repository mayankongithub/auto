#!/usr/bin/env python3
"""
Daily Job Search Automation Script
Searches for relevant job postings, filters using AI, and emails results
"""

import json
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from typing import List, Dict
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import configuration
from config import (
    GLM_API_KEY, SERPAPI_KEY, RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD,
    KEYWORDS, LOCATION, CANDIDATE_PROFILE, AI_MATCH_THRESHOLD,
    AI_MODEL, AI_TEMPERATURE, GLM_API_URL, SERPAPI_URL,
    RATE_LIMIT_BETWEEN_SEARCHES, RATE_LIMIT_BETWEEN_AI_CALLS,
    MAX_JOBS_PER_KEYWORD, RESULTS_FILENAME_TEMPLATE,
    get_candidate_summary
)


class JobSearcher:
    """Handles job searching across multiple platforms"""
    
    def __init__(self):
        self.jobs = []
    
    def search_serpapi(self, keyword: str) -> List[Dict]:
        """Search jobs using SerpAPI (Google Jobs)"""
        if not SERPAPI_KEY:
            print("Warning: SERPAPI_KEY not set, skipping SerpAPI search")
            return []

        try:
            params = {
                "engine": "google_jobs",
                "q": f"{keyword} India",
                "api_key": SERPAPI_KEY
            }

            response = requests.get(SERPAPI_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            jobs = []
            jobs_found = data.get("jobs_results", [])
            print(f"  Found {len(jobs_found)} jobs for '{keyword}'")

            for job in jobs_found[:MAX_JOBS_PER_KEYWORD]:
                jobs.append({
                    "title": job.get("title", ""),
                    "company": job.get("company_name", ""),
                    "location": job.get("location", ""),
                    "description": job.get("description", ""),
                    "link": job.get("share_link", job.get("apply_link", "")),
                    "source": "Google Jobs"
                })

            return jobs
        except Exception as e:
            print(f"Error searching SerpAPI for '{keyword}': {str(e)}")
            return []
    
    def search_all_keywords(self) -> List[Dict]:
        """Search all keywords across platforms"""
        all_jobs = []

        for keyword in KEYWORDS:
            print(f"Searching for: {keyword}")
            jobs = self.search_serpapi(keyword)
            all_jobs.extend(jobs)
            time.sleep(RATE_LIMIT_BETWEEN_SEARCHES)  # Rate limiting

        # Remove duplicates based on title and company
        unique_jobs = []
        seen = set()
        for job in all_jobs:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        return unique_jobs


class AIJobMatcher:
    """Uses GLM API to filter and match jobs against candidate profile"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = GLM_API_URL
    
    def analyze_job(self, job: Dict) -> Dict:
        """Analyze if job matches candidate profile using GLM AI"""
        try:
            candidate_summary = get_candidate_summary()

            prompt = f"""Analyze this job posting for a recent Computer Science graduate with the following profile:

{candidate_summary}

JOB POSTING:
Title: {job['title']}
Company: {job['company']}
Location: {job['location']}
Description: {job['description'][:1000]}

Evaluate:
1. Match Score (0-100): How well does this job match the candidate's profile?
2. Relevant: Is this suitable for a fresher/entry-level candidate? (Yes/No)
3. Key Matching Skills: List matching skills
4. Reason: Brief explanation

Respond in JSON format:
{{"match_score": <number>, "relevant": "<Yes/No>", "matching_skills": ["skill1", "skill2"], "reason": "<explanation>"}}"""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": AI_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": AI_TEMPERATURE
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            # Parse JSON response
            analysis = json.loads(content)
            job['match_score'] = analysis.get('match_score', 0)
            job['relevant'] = analysis.get('relevant', 'No')
            job['matching_skills'] = analysis.get('matching_skills', [])
            job['ai_reason'] = analysis.get('reason', '')

            return job

        except Exception as e:
            print(f"Error analyzing job {job['title']}: {str(e)}")
            # Default scoring on error
            job['match_score'] = 50
            job['relevant'] = 'Unknown'
            job['matching_skills'] = []
            job['ai_reason'] = 'Analysis failed'
            return job

    def filter_jobs(self, jobs: List[Dict], min_score: int = None) -> List[Dict]:
        """Filter jobs based on AI analysis"""
        if min_score is None:
            min_score = AI_MATCH_THRESHOLD

        filtered_jobs = []

        for job in jobs:
            print(f"Analyzing: {job['title']} at {job['company']}")
            analyzed_job = self.analyze_job(job)

            if analyzed_job['relevant'] == 'Yes' and analyzed_job['match_score'] >= min_score:
                filtered_jobs.append(analyzed_job)

            time.sleep(RATE_LIMIT_BETWEEN_AI_CALLS)  # Rate limiting

        # Sort by match score
        filtered_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        return filtered_jobs


class EmailNotifier:
    """Handles email notifications"""

    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def format_email_body(self, jobs: List[Dict]) -> str:
        """Format jobs into HTML email"""
        if not jobs:
            return """
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Daily Job Search Results</h2>
                    <p>No matching jobs found today. The search will continue tomorrow.</p>
                    <p><em>Date: {}</em></p>
                </body>
            </html>
            """.format(datetime.now().strftime("%Y-%m-%d"))

        jobs_html = ""
        for i, job in enumerate(jobs, 1):
            skills_badge = ', '.join(job.get('matching_skills', [])[:5])

            jobs_html += f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; background-color: #f9f9f9;">
                <h3 style="color: #2c3e50; margin: 0 0 10px 0;">{i}. {job['title']}</h3>
                <p style="margin: 5px 0;"><strong>Company:</strong> {job['company']}</p>
                <p style="margin: 5px 0;"><strong>Location:</strong> {job['location']}</p>
                <p style="margin: 5px 0;"><strong>Match Score:</strong> <span style="color: #27ae60; font-weight: bold;">{job['match_score']}%</span></p>
                <p style="margin: 5px 0;"><strong>Matching Skills:</strong> <em>{skills_badge}</em></p>
                <p style="margin: 5px 0;"><strong>AI Analysis:</strong> {job.get('ai_reason', 'N/A')}</p>
                <p style="margin: 10px 0 0 0;">
                    <a href="{job['link']}" style="background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Apply Now</a>
                </p>
            </div>
            """

        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
                <h2 style="color: #2c3e50;">🎯 Daily Job Search Results for Mayank Sharma</h2>
                <p><strong>Date:</strong> {datetime.now().strftime("%Y-%m-%d")}</p>
                <p><strong>Total Matches Found:</strong> {len(jobs)}</p>
                <hr style="border: 1px solid #ddd;">
                {jobs_html}
                <hr style="border: 1px solid #ddd;">
                <p style="color: #7f8c8d; font-size: 12px;">
                    <em>This is an automated job search based on your resume. Jobs are filtered using AI to match your skills: C/C++, JavaScript, Node.js, MongoDB, Distributed Systems.</em>
                </p>
            </body>
        </html>
        """
        return html

    def send_email(self, recipient: str, jobs: List[Dict]):
        """Send email with job results"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Daily Job Alert - {len(jobs)} Matches Found ({datetime.now().strftime('%Y-%m-%d')})"
            msg['From'] = self.sender_email
            msg['To'] = recipient

            html_body = self.format_email_body(jobs)
            msg.attach(MIMEText(html_body, 'html'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"✅ Email sent successfully to {recipient}")

        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")


def main():
    """Main execution function"""
    print("=" * 60)
    print("🚀 Starting Daily Job Search Automation")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print("=" * 60)

    # Step 1: Search for jobs
    print("\n[1/4] Searching job boards...")
    searcher = JobSearcher()
    jobs = searcher.search_all_keywords()
    print(f"✅ Found {len(jobs)} total jobs")

    # Step 2: Filter with AI
    print("\n[2/4] Analyzing jobs with GLM AI...")
    ai_matcher = AIJobMatcher(GLM_API_KEY)
    filtered_jobs = ai_matcher.filter_jobs(jobs)
    print(f"✅ Filtered to {len(filtered_jobs)} relevant jobs")

    # Step 3: Send email
    print("\n[3/4] Preparing email notification...")
    if SENDER_EMAIL and SENDER_PASSWORD:
        notifier = EmailNotifier(SENDER_EMAIL, SENDER_PASSWORD)
        notifier.send_email(RECIPIENT_EMAIL, filtered_jobs)
    else:
        print("⚠️  Email credentials not set. Skipping email notification.")
        print(f"Found {len(filtered_jobs)} jobs to report")

    # Step 4: Save results
    print("\n[4/4] Saving results...")
    output_file = RESULTS_FILENAME_TEMPLATE.format(date=datetime.now().strftime('%Y%m%d'))
    with open(output_file, 'w') as f:
        json.dump(filtered_jobs, f, indent=2)
    print(f"✅ Results saved to {output_file}")

    print("\n" + "=" * 60)
    print("✨ Job search automation completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

