#!/usr/bin/env python3
"""
Direct Career Page Job Search Automation
Searches company career pages for active job postings
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
import re

# Load environment variables
load_dotenv()

from config import (
    SERPAPI_KEY, RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD,
    KEYWORDS, SERPAPI_URL, RATE_LIMIT_BETWEEN_SEARCHES,
    MAX_JOBS_PER_KEYWORD, RESULTS_FILENAME_TEMPLATE
)

# Major companies with direct career pages in India
COMPANIES_INDIA = [
    {"name": "Google", "careers_url": "https://www.google.com/about/careers/applications/jobs/results/", "api": "google"},
    {"name": "Microsoft", "careers_url": "https://careers.microsoft.com/professionals/us/en/search-results", "location": "India"},
    {"name": "Amazon", "careers_url": "https://www.amazon.jobs/en/search.json", "location": "India"},
    {"name": "Flipkart", "careers_url": "https://www.flipkartcareers.com/", "location": "India"},
    {"name": "Swiggy", "careers_url": "https://careers.swiggy.com/", "location": "India"},
    {"name": "Zomato", "careers_url": "https://www.zomato.com/careers", "location": "India"},
    {"name": "Paytm", "careers_url": "https://paytm.com/careers", "location": "India"},
    {"name": "PhonePe", "careers_url": "https://www.phonepe.com/careers/", "location": "India"},
    {"name": "Razorpay", "careers_url": "https://razorpay.com/jobs/", "location": "India"},
    {"name": "CRED", "careers_url": "https://careers.cred.club/", "location": "India"},
]

# Job keywords for fresher/entry-level
FRESHER_KEYWORDS = ["fresher", "entry level", "junior", "graduate", "trainee", "associate", "sde-1", "sde 1"]


class JobSearcher:
    """Handles job searching from career pages"""

    def __init__(self):
        self.jobs = []

    def search_linkedin_jobs(self, keyword: str) -> List[Dict]:
        """Search LinkedIn Jobs using SerpAPI"""
        if not SERPAPI_KEY:
            print("Warning: SERPAPI_KEY not set")
            return []

        try:
            params = {
                "engine": "linkedin_jobs",
                "q": f"{keyword}",
                "location": "India",
                "api_key": SERPAPI_KEY
            }

            response = requests.get(SERPAPI_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            jobs = []
            jobs_found = data.get("jobs_results", [])
            print(f"  LinkedIn: Found {len(jobs_found)} jobs for '{keyword}'")

            for job in jobs_found[:5]:  # Get top 5 from LinkedIn
                title = job.get("title", "").lower()
                description = job.get("description", "").lower()

                # Filter for fresher/entry-level
                senior_keywords = ["senior", "lead", "manager", "architect", "principal", "staff", "sr.", "sr ", "5+ years", "6+ years", "7+ years", "8+ years"]
                fresher_keywords = ["fresher", "entry level", "entry-level", "junior", "graduate", "0-1 year", "0-2 year", "trainee", "intern", "sde 1", "sde-1", "sde i"]

                is_senior = any(kw in title or kw in description[:300] for kw in senior_keywords)
                is_fresher = any(kw in title or kw in description[:300] for kw in fresher_keywords)

                if not is_senior or is_fresher:
                    # Extract job ID and create direct LinkedIn link
                    job_id = job.get("job_id", "")
                    direct_link = f"https://www.linkedin.com/jobs/view/{job_id}" if job_id else job.get("link", "")

                    jobs.append({
                        "title": job.get("title", ""),
                        "company": job.get("company_name", ""),
                        "location": job.get("location", ""),
                        "description": job.get("description", "")[:500],
                        "link": direct_link,
                        "source": "LinkedIn",
                        "posted_date": job.get("detected_extensions", {}).get("posted_at", "Recently")
                    })

            return jobs
        except Exception as e:
            print(f"  LinkedIn Error: {str(e)}")
            return []

    def search_indeed_jobs(self, keyword: str) -> List[Dict]:
        """Search Indeed Jobs using SerpAPI"""
        if not SERPAPI_KEY:
            return []

        try:
            params = {
                "engine": "indeed_jobs",
                "q": f"{keyword} fresher",
                "location": "India",
                "api_key": SERPAPI_KEY
            }

            response = requests.get(SERPAPI_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            jobs = []
            jobs_found = data.get("jobs_results", [])
            print(f"  Indeed: Found {len(jobs_found)} jobs for '{keyword}'")

            for job in jobs_found[:5]:  # Get top 5 from Indeed
                title = job.get("title", "").lower()
                description = job.get("description", "").lower()

                # Filter for fresher/entry-level
                senior_keywords = ["senior", "lead", "manager", "architect", "principal", "staff", "sr.", "sr ", "5+ years", "6+ years", "7+ years"]
                is_senior = any(kw in title for kw in senior_keywords)

                if not is_senior:
                    # Get direct Indeed link
                    direct_link = job.get("link", "")

                    jobs.append({
                        "title": job.get("title", ""),
                        "company": job.get("company_name", ""),
                        "location": job.get("location", ""),
                        "description": job.get("description", "")[:500],
                        "link": direct_link,
                        "source": "Indeed",
                        "posted_date": job.get("detected_extensions", {}).get("posted_at", "Recently")
                    })

            return jobs
        except Exception as e:
            print(f"  Indeed Error: {str(e)}")
            return []
    
    def search_all_keywords(self) -> List[Dict]:
        """Search all keywords across LinkedIn and Indeed"""
        all_jobs = []

        # Focus on most relevant keywords for freshers
        fresher_keywords = [
            "Software Engineer Fresher",
            "Backend Developer Entry Level",
            "C++ Developer Fresher",
            "Node.js Developer Junior",
            "Full Stack Developer Graduate"
        ]

        for keyword in fresher_keywords:
            print(f"\nSearching for: {keyword}")

            # Search LinkedIn
            linkedin_jobs = self.search_linkedin_jobs(keyword)
            all_jobs.extend(linkedin_jobs)
            time.sleep(1)

            # Search Indeed
            indeed_jobs = self.search_indeed_jobs(keyword)
            all_jobs.extend(indeed_jobs)
            time.sleep(RATE_LIMIT_BETWEEN_SEARCHES)

        # Remove duplicates based on title and company
        unique_jobs = []
        seen = set()
        for job in all_jobs:
            key = (job['title'].lower().strip(), job['company'].lower().strip())
            if key not in seen and job.get('link'):  # Only include jobs with valid links
                seen.add(key)
                unique_jobs.append(job)

        # Sort by source priority (LinkedIn first, then Indeed)
        unique_jobs.sort(key=lambda x: (x['source'] != 'LinkedIn', x.get('posted_date', '')), reverse=False)

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
            source_badge = f"<span style='background-color: #0077b5; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; margin-left: 10px;'>{job.get('source', 'Job Board')}</span>"
            posted_date = job.get('posted_date', 'Recently posted')

            jobs_html += f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; background-color: #f9f9f9;">
                <h3 style="margin: 0 0 10px 0; color: #2c3e50;">{i}. {job['title']} {source_badge}</h3>
                <p style="margin: 5px 0;"><strong>🏢 Company:</strong> {job['company']}</p>
                <p style="margin: 5px 0;"><strong>📍 Location:</strong> {job['location']}</p>
                <p style="margin: 5px 0;"><strong>🕐 Posted:</strong> {posted_date}</p>
                <p style="margin: 10px 0; color: #555;">{job['description'][:250]}...</p>
                <p style="margin: 15px 0 0 0;">
                    <a href="{job['link']}" target="_blank" style="background-color: #0077b5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">🔗 Apply on {job.get('source', 'Website')}</a>
                </p>
            </div>
            """

        html = f"""<html><body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">🎯 Daily Job Search Results for Mayank Sharma</h2>
                <p><strong>📅 Date:</strong> {datetime.now().strftime("%B %d, %Y")}</p>
                <p><strong>📊 Total Active Jobs:</strong> {len(jobs)} fresher/entry-level positions</p>
                <p style="background-color: #e8f5e9; padding: 10px; border-left: 4px solid #4caf50; margin: 15px 0;">
                    ✅ <strong>Filtered for:</strong> Fresher, Entry-level, 0-1 year experience<br>
                    ✅ <strong>Sources:</strong> LinkedIn, Indeed (Direct career page links)<br>
                    ✅ <strong>Location:</strong> India only
                </p>
                <hr style="border: 1px solid #ddd; margin: 20px 0;">{jobs_html}<hr style="border: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #7f8c8d; font-size: 12px; text-align: center;"><em>🤖 Automated daily job search • Direct career page links • Fresher-focused filtering</em></p>
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
        print("📧 To enable email:")
        print("   1. Generate Gmail App Password at https://myaccount.google.com/security")
        print("   2. Add GitHub Secrets: SENDER_EMAIL and SENDER_PASSWORD")
    
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
