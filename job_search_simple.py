#!/usr/bin/env python3
"""
Direct Company Career Page Job Search
ONLY gets jobs from official company career portals
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
    SERPAPI_URL, RATE_LIMIT_BETWEEN_SEARCHES, RESULTS_FILENAME_TEMPLATE
)

# Top tech companies in India with career pages
TOP_COMPANIES_INDIA = [
    # FAANG & Big Tech
    "Google", "Microsoft", "Amazon", "Meta", "Apple",
    # Indian Tech Giants
    "Flipkart", "Swiggy", "Zomato", "Paytm", "PhonePe", "Razorpay", "CRED",
    "Ola", "Uber", "Dunzo", "Zepto", "Meesho", "Myntra", "Nykaa",
    # Fintech
    "BharatPe", "PolicyBazaar", "Groww", "Upstox", "Sharechat", "MobiKwik",
    # Edtech & SaaS
    "BYJU'S", "Unacademy", "Vedantu", "upGrad", "Freshworks", "Zoho", "Postman",
    # Product Companies
    "Adobe", "Atlassian", "Salesforce", "Oracle", "SAP", "VMware", "Intuit",
    "Intel", "NVIDIA", "Qualcomm", "Cisco", "Dell", "HP",
    # Consulting & Services
    "Accenture", "TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra", "Capgemini",
    # E-commerce & Delivery
    "Snapdeal", "Licious", "BigBasket", "Urban Company", "Cure.fit",
    # Gaming & Entertainment
    "Dream11", "MPL", "Hike", "ShareChat", "Glance",
    # Emerging Startups
    "Udaan", "Zetwerk", "ApnaKlub", "CARS24", "Delhivery", "BlackBuck"
]

# Job keywords for fresher/entry-level
FRESHER_KEYWORDS = ["fresher", "entry level", "junior", "graduate", "trainee", "associate", "sde-1", "sde 1"]


class JobSearcher:
    """Handles job searching from company career pages ONLY"""

    def __init__(self):
        self.jobs = []

    def get_amazon_jobs(self) -> List[Dict]:
        """Get jobs DIRECTLY from Amazon careers API"""
        try:
            url = "https://www.amazon.jobs/en/search.json"
            params = {
                "offset": 0,
                "result_limit": 20,
                "sort": "recent",
                "country[]": "IND",
                "category[]": "software-development"
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            jobs = []
            for job in data.get("jobs", []):
                title = job.get("title", "").lower()

                # Filter for entry-level (exclude senior/manager)
                if any(kw in title for kw in ["senior", "sr.", "manager", "principal", "lead"]):
                    continue

                # Include entry-level keywords
                if any(kw in title for kw in ["software development engineer", "sde", "software engineer"]):
                    jobs.append({
                        "title": job.get("title", ""),
                        "company": "Amazon",
                        "location": job.get("location", ""),
                        "description": job.get("description_short", "")[:500],
                        "link": f"https://www.amazon.jobs{job.get('job_path', '')}",
                        "source": "Amazon Careers",
                        "posted_date": job.get("posted_date", "Recently")
                    })

            print(f"  ✅ Amazon: {len(jobs)} jobs")
            return jobs
        except Exception as e:
            print(f"  ❌ Amazon Error: {str(e)}")
            return []

    def extract_apply_link(self, job: Dict) -> str:
        """Extract the actual apply link from job data"""
        # Try to get apply link from extensions
        extensions = job.get("detected_extensions", {})
        if "apply_link" in extensions:
            return extensions["apply_link"]

        # Try related links for company career page
        related_links = job.get("related_links", [])
        for link in related_links:
            if any(keyword in link.get("link", "").lower() for keyword in ["career", "jobs", "apply", "linkedin.com/jobs", "naukri.com", "instahyre"]):
                return link.get("link", "")

        # Fallback to share link
        return job.get("share_link", job.get("apply_link", ""))

    def is_fresher_job(self, title: str, description: str) -> bool:
        """Check if job is suitable for freshers"""
        title_lower = title.lower()
        desc_lower = description[:400].lower()

        # Exclude senior positions
        senior_keywords = ["senior", "lead", "manager", "architect", "principal", "staff", "sr.", "sr ",
                          "5+ years", "6+ years", "7+ years", "8+ years", "10+ years",
                          "experienced", "expert", "specialist"]

        # Look for fresher indicators
        fresher_keywords = ["fresher", "entry level", "entry-level", "junior", "graduate",
                           "0-1 year", "0-2 year", "trainee", "intern", "sde 1", "sde-1",
                           "sde i", "associate", "campus", "recent graduate"]

        # Strong exclusion if title has senior keywords
        if any(kw in title_lower for kw in senior_keywords):
            return False

        # Include if fresher keywords present
        if any(kw in title_lower or kw in desc_lower for kw in fresher_keywords):
            return True

        # Exclude if description mentions years of experience
        if any(kw in desc_lower for kw in ["5+ years", "6+ years", "7+ years", "experience required", "years of experience"]):
            return False

        return True  # Include by default if no exclusions

    def search_company_direct_careers(self, company_name: str) -> List[Dict]:
        """Search for jobs but ONLY accept direct company career page links"""
        if not SERPAPI_KEY:
            return []

        try:
            params = {
                "engine": "google_jobs",
                "q": f"{company_name} software engineer fresher India",
                "api_key": SERPAPI_KEY
            }

            response = requests.get(SERPAPI_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            jobs = []
            for job in data.get("jobs_results", [])[:10]:
                # CRITICAL: Only accept jobs from company's actual career page
                company = job.get("company_name", "")
                if company_name.lower() not in company.lower():
                    continue  # Skip if not from actual company

                title = job.get("title", "")
                description = job.get("description", "")

                # Filter for fresher
                if not self.is_fresher_job(title, description):
                    continue

                # Extract link - MUST be from company's career domain
                link = job.get("apply_link", job.get("share_link", ""))

                # Try to find company career page link in related_links
                related_links = job.get("related_links", [])
                company_career_link = None

                for link_obj in related_links:
                    url = link_obj.get("link", "").lower()
                    # Accept ONLY if it's the company's official career domain
                    if any(domain in url for domain in [
                        f"{company_name.lower()}.com/careers",
                        f"{company_name.lower()}.com/jobs",
                        f"careers.{company_name.lower()}.com",
                        f"jobs.{company_name.lower()}.com",
                        "amazon.jobs", "careers.microsoft.com", "careers.google.com",
                        "flipkartcareers.com", "careers.swiggy.com"
                    ]):
                        company_career_link = link_obj.get("link", "")
                        break

                # ONLY include if we found a direct company career page link
                if not company_career_link:
                    continue  # Skip third-party job board links

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": job.get("location", ""),
                    "description": description[:500],
                    "link": company_career_link,  # Use direct career page link only
                    "source": f"{company_name} Careers",
                    "posted_date": job.get("detected_extensions", {}).get("posted_at", "Recently")
                })

            if jobs:
                print(f"  ✅ {company_name}: {len(jobs)} direct career page jobs")
            return jobs
        except Exception as e:
            return []

    def search_company_careers(self, company_name: str) -> List[Dict]:
        """Search specific company career pages for fresher jobs"""
        if not SERPAPI_KEY:
            return []

        try:
            # Search for company career page jobs
            params = {
                "engine": "google_jobs",
                "q": f"{company_name} fresher software engineer India",
                "api_key": SERPAPI_KEY
            }

            response = requests.get(SERPAPI_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            jobs = []
            jobs_found = data.get("jobs_results", [])

            for job in jobs_found[:5]:  # Top 5 from each company
                # Only include jobs from the actual company
                company = job.get("company_name", "")
                if company_name.lower() not in company.lower():
                    continue

                title = job.get("title", "")
                description = job.get("description", "")

                # Filter for fresher jobs
                if not self.is_fresher_job(title, description):
                    continue

                # Extract best apply link
                apply_link = job.get("apply_link", "")
                if not apply_link:
                    apply_link = job.get("share_link", "")

                # Try to find company career page link
                related_links = job.get("related_links", [])
                for link_obj in related_links:
                    link = link_obj.get("link", "")
                    # Prefer company career pages
                    if any(domain in link.lower() for domain in ["careers.", "jobs.", company_name.lower()]):
                        apply_link = link
                        break

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": job.get("location", ""),
                    "description": description[:500],
                    "link": apply_link,
                    "source": f"{company_name} Careers",
                    "posted_date": job.get("detected_extensions", {}).get("posted_at", "Recently posted")
                })

            return jobs
        except Exception as e:
            return []

    def search_google_jobs_filtered(self, keyword: str) -> List[Dict]:
        """Search Google Jobs with better filtering for direct links"""
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
            print(f"  Found {len(jobs_found)} jobs, filtering...")

            for job in jobs_found[:15]:  # Check more jobs to get good ones after filtering
                title = job.get("title", "")
                description = job.get("description", "")

                # Filter for fresher jobs
                if not self.is_fresher_job(title, description):
                    continue

                # Extract best apply link - prefer via links
                apply_link = job.get("apply_link", "")
                if not apply_link:
                    apply_link = job.get("share_link", "")

                # Try to find better links in related_links
                related_links = job.get("related_links", [])
                for link_obj in related_links:
                    link = link_obj.get("link", "")
                    # Prefer direct career page links
                    if any(domain in link for domain in ["linkedin.com/jobs/view", "naukri.com/job", "instahyre.com", "indeed.com/viewjob", "careers.", "jobs."]):
                        apply_link = link
                        break

                # Determine source from link
                source = "Career Page"
                if "linkedin.com" in apply_link.lower():
                    source = "LinkedIn"
                elif "naukri.com" in apply_link.lower():
                    source = "Naukri"
                elif "instahyre.com" in apply_link.lower():
                    source = "Instahyre"
                elif "indeed.com" in apply_link.lower():
                    source = "Indeed"
                elif "careers." in apply_link.lower() or "jobs." in apply_link.lower():
                    source = "Company Career Page"

                jobs.append({
                    "title": title,
                    "company": job.get("company_name", ""),
                    "location": job.get("location", ""),
                    "description": description[:500],
                    "link": apply_link,
                    "source": source,
                    "posted_date": job.get("detected_extensions", {}).get("posted_at", "Recently posted")
                })

                # Stop after finding enough good jobs
                if len(jobs) >= MAX_JOBS_PER_KEYWORD:
                    break

            print(f"  ✅ {len(jobs)} fresher jobs after filtering")
            return jobs
        except Exception as e:
            print(f"  Error: {str(e)}")
            return []
    
    def search_all_keywords(self) -> List[Dict]:
        """Search ONLY direct company career pages"""
        all_jobs = []

        print("\n🏢 DIRECT COMPANY CAREER PAGE SEARCH")
        print("=" * 60)
        print("🎯 Getting jobs ONLY from official company portals")
        print("✅ NO third-party job boards or aggregators\n")

        # Part 1: Amazon direct API
        print("\n[1/11] Amazon (Direct API)...")
        all_jobs.extend(self.get_amazon_jobs())
        time.sleep(RATE_LIMIT_BETWEEN_SEARCHES)

        # Part 2: Top companies with direct career page filtering
        top_companies = [
            "Microsoft", "Google", "Meta", "Adobe", "Atlassian",
            "Flipkart", "Swiggy", "Zomato", "Razorpay", "CRED"
        ]

        for i, company in enumerate(top_companies, 2):
            print(f"\n[{i}/11] {company} (Career Page Only)...")
            company_jobs = self.search_company_direct_careers(company)
            all_jobs.extend(company_jobs)
            time.sleep(RATE_LIMIT_BETWEEN_SEARCHES)

        print(f"\n" + "=" * 60)
        print(f"📊 Total jobs found: {len(all_jobs)}")

        # Remove duplicates
        unique_jobs = []
        seen = set()
        for job in all_jobs:
            key = (job['title'].lower().strip(), job['company'].lower().strip())
            if key not in seen and job.get('link'):
                seen.add(key)
                unique_jobs.append(job)

        print(f"✅ Unique jobs after deduplication: {len(unique_jobs)}")
        print("=" * 60)

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
