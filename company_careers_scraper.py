#!/usr/bin/env python3
"""
Direct Company Career Page Scraper
Gets jobs ONLY from official company career portals
"""

import json
import requests
from datetime import datetime
from typing import List, Dict
import time
from dotenv import load_dotenv

load_dotenv()

from config import RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD

# Company career page APIs and URLs (direct sources only)
COMPANY_CAREER_APIS = [
    {
        "name": "Google",
        "api_url": "https://careers.google.com/api/v3/search/",
        "params": {"location": "India", "q": "Software Engineer", "employment_type": "FULL_TIME"},
        "job_url_template": "https://careers.google.com/jobs/results/{job_id}/"
    },
    {
        "name": "Microsoft",
        "api_url": "https://gcsservices.careers.microsoft.com/search/api/v1/search",
        "params": {"lc": "India", "q": "Software Engineer"},
        "job_url_template": "https://careers.microsoft.com/us/en/job/{job_id}/"
    },
    {
        "name": "Amazon",
        "api_url": "https://www.amazon.jobs/en/search.json",
        "params": {"country": "IND", "normalized_country_code": "IND"},
        "job_url_template": "https://www.amazon.jobs/en/jobs/{job_id}/"
    },
    {
        "name": "Adobe",
        "search_url": "https://careers.adobe.com/us/en/search-results?keywords=software%20engineer&location=India",
        "job_url_template": "https://careers.adobe.com/us/en/job/{job_id}/"
    },
    {
        "name": "Atlassian",
        "search_url": "https://www.atlassian.com/company/careers/all-jobs",
        "location_filter": "India"
    },
    {
        "name": "Salesforce",
        "search_url": "https://salesforce.wd1.myworkdayjobs.com/External_Career_Site",
        "location_filter": "India"
    }
]

# Indian company career pages
INDIAN_COMPANIES = [
    {"name": "Flipkart", "url": "https://www.flipkartcareers.com/", "search_term": "software engineer fresher"},
    {"name": "Swiggy", "url": "https://careers.swiggy.com/", "search_term": "software engineer"},
    {"name": "Zomato", "url": "https://www.zomato.com/careers", "search_term": "engineer"},
    {"name": "Razorpay", "url": "https://razorpay.com/jobs/", "search_term": "software engineer"},
    {"name": "CRED", "url": "https://careers.cred.club/", "search_term": "engineer"},
    {"name": "PhonePe", "url": "https://www.phonepe.com/careers/", "search_term": "software"},
    {"name": "Paytm", "url": "https://paytm.com/careers", "search_term": "software engineer"},
    {"name": "Freshworks", "url": "https://www.freshworks.com/company/careers/", "search_term": "engineer"},
    {"name": "Zoho", "url": "https://www.zoho.com/careers/", "search_term": "software"},
    {"name": "Postman", "url": "https://www.postman.com/company/careers/", "search_term": "engineer"}
]


def get_amazon_jobs() -> List[Dict]:
    """Get jobs directly from Amazon careers API"""
    try:
        url = "https://www.amazon.jobs/en/search.json"
        params = {
            "offset": 0,
            "result_limit": 10,
            "sort": "recent",
            "country[]": "IND",
            "category[]": "software-development",
            "job_title[]": "software-dev-engineer-i"  # Entry level
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        jobs = []
        for job in data.get("jobs", [])[:10]:
            jobs.append({
                "title": job.get("title", ""),
                "company": "Amazon",
                "location": job.get("location", ""),
                "description": job.get("description_short", "")[:500],
                "link": f"https://www.amazon.jobs{job.get('job_path', '')}",
                "source": "Amazon Careers",
                "posted_date": job.get("posted_date", "Recently")
            })
        
        print(f"  Amazon: Found {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"  Amazon Error: {str(e)}")
        return []


def get_microsoft_jobs() -> List[Dict]:
    """Get jobs directly from Microsoft careers"""
    try:
        url = "https://gcsservices.careers.microsoft.com/search/api/v1/search"
        payload = {
            "lang": "en_us",
            "pgSz": 20,
            "pgNum": 1,
            "filters": [
                {"id": "locationsString", "values": ["India"]},
                {"id": "jobTypeString", "values": ["Full-Time"]}
            ],
            "keyword": "Software Engineer"
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        jobs = []
        for job in data.get("operationResult", {}).get("result", {}).get("jobs", [])[:10]:
            title = job.get("title", "").lower()
            # Filter for fresher/entry level
            if any(kw in title for kw in ["senior", "principal", "lead", "manager"]):
                continue

            jobs.append({
                "title": job.get("title", ""),
                "company": "Microsoft",
                "location": job.get("location", ""),
                "description": job.get("description", "")[:500],
                "link": f"https://jobs.careers.microsoft.com/global/en/job/{job.get('jobId', '')}/",
                "source": "Microsoft Careers",
                "posted_date": "Recently"
            })

        print(f"  Microsoft: Found {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"  Microsoft Error: {str(e)}")
        return []


def get_adobe_jobs() -> List[Dict]:
    """Get jobs from Adobe careers"""
    try:
        # Adobe uses a different system, we'll use their search page
        url = "https://careers.adobe.com/us/en/search-results"
        params = {"keywords": "software engineer", "location": "India"}

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers, timeout=30)

        # For now, return empty as Adobe requires complex scraping
        # Will add LinkedIn/Naukri aggregation for Adobe jobs
        print(f"  Adobe: Requires advanced scraping (skipping)")
        return []
    except Exception as e:
        print(f"  Adobe Error: {str(e)}")
        return []


def get_all_company_jobs() -> List[Dict]:
    """Get jobs from all company career pages"""
    all_jobs = []

    print("\n🏢 Checking Company Career Pages Directly")
    print("=" * 60)

    # Amazon
    print("\n[1/3] Amazon Careers...")
    all_jobs.extend(get_amazon_jobs())
    time.sleep(2)

    # Microsoft
    print("\n[2/3] Microsoft Careers...")
    all_jobs.extend(get_microsoft_jobs())
    time.sleep(2)

    # Adobe
    print("\n[3/3] Adobe Careers...")
    all_jobs.extend(get_adobe_jobs())
    time.sleep(2)

    # Remove duplicates
    unique_jobs = []
    seen = set()
    for job in all_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    print(f"\n✅ Total: {len(unique_jobs)} unique jobs from company career pages")
    return unique_jobs


if __name__ == "__main__":
    jobs = get_all_company_jobs()
    print(f"\nFound {len(jobs)} jobs")
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Link: {job['link']}")
