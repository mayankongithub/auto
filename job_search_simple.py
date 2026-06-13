#!/usr/bin/env python3
"""
Simple Job Search Automation (Without AI Filtering)
Searches for relevant job postings and emails results
"""

import json
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from typing import List, Dict
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import (
    SERPAPI_KEY, RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD,
    KEYWORDS, SERPAPI_URL, RATE_LIMIT_BETWEEN_SEARCHES,
    MAX_JOBS_PER_KEYWORD, RESULTS_FILENAME_TEMPLATE
)


class JobSearcher:
    """Handles job searching"""
    
    def __init__(self):
        self.jobs = []
    
    def search_serpapi(self, keyword: str) -> List[Dict]:
        """Search jobs using SerpAPI"""
        if not SERPAPI_KEY:
            print("Warning: SERPAPI_KEY not set")
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
                    "description": job.get("description", "")[:500],
                    "link": job.get("share_link", job.get("apply_link", "")),
                    "source": "Google Jobs"
                })
            
            return jobs
        except Exception as e:
            print(f"Error searching for '{keyword}': {str(e)}")
            return []
    
    def search_all_keywords(self) -> List[Dict]:
        """Search all keywords"""
        all_jobs = []
        
        for keyword in KEYWORDS:
            print(f"Searching for: {keyword}")
            jobs = self.search_serpapi(keyword)
            all_jobs.extend(jobs)
            time.sleep(RATE_LIMIT_BETWEEN_SEARCHES)
        
        # Remove duplicates
        unique_jobs = []
        seen = set()
        for job in all_jobs:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs


class EmailNotifier:
    """Handles email notifications"""
    
    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def format_email_body(self, jobs: List[Dict]) -> str:
        """Format jobs into HTML email"""
        if not jobs:
            return f"""<html><body><h2>Daily Job Search Results</h2>
            <p>No jobs found today.</p><p><em>Date: {datetime.now().strftime("%Y-%m-%d")}</em></p>
            </body></html>"""
        
        jobs_html = ""
        for i, job in enumerate(jobs, 1):
            jobs_html += f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h3>{i}. {job['title']}</h3>
                <p><strong>Company:</strong> {job['company']}</p>
                <p><strong>Location:</strong> {job['location']}</p>
                <p><strong>Description:</strong> {job['description'][:200]}...</p>
                <p><a href="{job['link']}" style="background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Apply Now</a></p>
            </div>
            """
        
        html = f"""<html><body style="font-family: Arial, sans-serif;">
                <h2>🎯 Daily Job Search Results for Mayank Sharma</h2>
                <p><strong>Date:</strong> {datetime.now().strftime("%Y-%m-%d")}</p>
                <p><strong>Total Jobs Found:</strong> {len(jobs)}</p>
                <hr>{jobs_html}<hr>
                <p style="color: #7f8c8d; font-size: 12px;"><em>Automated job search for Software Engineer positions in India.</em></p>
                </body></html>"""
        return html
    
    def send_email(self, recipient: str, jobs: List[Dict]):
        """Send email with job results"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Daily Job Alert - {len(jobs)} Jobs Found ({datetime.now().strftime('%Y-%m-%d')})"
            msg['From'] = self.sender_email
            msg['To'] = recipient
            
            html_body = self.format_email_body(jobs)
            msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {recipient}")
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")


def main():
    """Main execution"""
    print("=" * 60)
    print("🚀 Starting Job Search Automation")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    print("\n[1/3] Searching job boards...")
    searcher = JobSearcher()
    jobs = searcher.search_all_keywords()
    print(f"✅ Found {len(jobs)} unique jobs")
    
    print("\n[2/3] Sending email notification...")
    if SENDER_EMAIL and SENDER_PASSWORD:
        notifier = EmailNotifier(SENDER_EMAIL, SENDER_PASSWORD)
        notifier.send_email(RECIPIENT_EMAIL, jobs)
    else:
        print("⚠️  Email credentials not set. Results saved to file only.")
    
    print("\n[3/3] Saving results...")
    output_file = RESULTS_FILENAME_TEMPLATE.format(date=datetime.now().strftime('%Y%m%d'))
    with open(output_file, 'w') as f:
        json.dump(jobs, f, indent=2)
    print(f"✅ Results saved to {output_file}")
    
    print("\n" + "=" * 60)
    print("✨ Job search completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
