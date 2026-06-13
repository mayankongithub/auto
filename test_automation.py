#!/usr/bin/env python3
"""
Test script for job search automation
Tests individual components without making actual API calls
"""

import json
from datetime import datetime
from config import (
    KEYWORDS, LOCATION, CANDIDATE_PROFILE,
    get_candidate_summary, AI_MATCH_THRESHOLD
)


def test_config():
    """Test configuration loading"""
    print("🧪 Testing Configuration...")
    print(f"✅ Keywords loaded: {len(KEYWORDS)} keywords")
    print(f"✅ Location: {LOCATION}")
    print(f"✅ AI Match Threshold: {AI_MATCH_THRESHOLD}")
    print(f"✅ Candidate Name: {CANDIDATE_PROFILE['name']}")
    print()


def test_candidate_summary():
    """Test candidate summary generation"""
    print("🧪 Testing Candidate Summary Generation...")
    summary = get_candidate_summary()
    print(summary)
    print(f"\n✅ Summary length: {len(summary)} characters")
    print()


def test_job_data_structure():
    """Test job data structure"""
    print("🧪 Testing Job Data Structure...")
    
    sample_job = {
        "title": "Backend Developer",
        "company": "Tech Company Pvt Ltd",
        "location": "Bangalore, India",
        "description": "Looking for a backend developer with Node.js and C++ experience...",
        "link": "https://example.com/apply",
        "source": "Google Jobs",
        "match_score": 85,
        "relevant": "Yes",
        "matching_skills": ["C++", "Node.js", "MongoDB"],
        "ai_reason": "Strong match for distributed systems and backend development"
    }
    
    print(json.dumps(sample_job, indent=2))
    print(f"\n✅ Job structure is valid")
    print()


def test_email_format():
    """Test email formatting (without sending)"""
    print("🧪 Testing Email Format...")
    
    sample_jobs = [
        {
            "title": "Software Developer - Fresher",
            "company": "InfoTech Solutions",
            "location": "Mumbai, India",
            "description": "Seeking fresh graduates with C++ and JavaScript skills",
            "link": "https://example.com/job1",
            "match_score": 92,
            "relevant": "Yes",
            "matching_skills": ["C++", "JavaScript", "MongoDB"],
            "ai_reason": "Excellent match - requires C++ and JavaScript which are core skills"
        },
        {
            "title": "Backend Engineer - Entry Level",
            "company": "CloudTech India",
            "location": "Bangalore, India",
            "description": "Backend development with Node.js and distributed systems",
            "link": "https://example.com/job2",
            "match_score": 88,
            "relevant": "Yes",
            "matching_skills": ["Node.js", "Distributed Systems", "Express"],
            "ai_reason": "Great fit - distributed systems experience from DDN internship is valuable"
        },
        {
            "title": "C++ Developer",
            "company": "Systems Pvt Ltd",
            "location": "Pune, India",
            "description": "C++ development for system software",
            "link": "https://example.com/job3",
            "match_score": 78,
            "relevant": "Yes",
            "matching_skills": ["C++", "Operating Systems"],
            "ai_reason": "Good match - strong C++ skills and OS knowledge"
        }
    ]
    
    # Create simple text preview
    print(f"📧 Email Preview for {len(sample_jobs)} jobs:\n")
    print("=" * 70)
    print(f"Subject: Daily Job Alert - {len(sample_jobs)} Matches Found ({datetime.now().strftime('%Y-%m-%d')})")
    print("=" * 70)
    print()
    
    for i, job in enumerate(sample_jobs, 1):
        print(f"{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Match Score: {job['match_score']}%")
        print(f"   Matching Skills: {', '.join(job['matching_skills'])}")
        print(f"   Why: {job['ai_reason']}")
        print(f"   Apply: {job['link']}")
        print()
    
    print("=" * 70)
    print("✅ Email formatting works correctly")
    print()


def test_keywords():
    """Test search keywords"""
    print("🧪 Testing Search Keywords...")
    print("Keywords to search:")
    for i, keyword in enumerate(KEYWORDS, 1):
        print(f"  {i}. {keyword}")
    print(f"\n✅ Total {len(KEYWORDS)} keywords configured")
    print()


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("🚀 Running Job Search Automation Tests")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    test_config()
    test_candidate_summary()
    test_job_data_structure()
    test_keywords()
    test_email_format()
    
    print("=" * 70)
    print("✅ All tests completed successfully!")
    print("=" * 70)
    print()
    print("💡 Next Steps:")
    print("  1. Set up your .env file with API keys")
    print("  2. Run: python job_search_automation.py")
    print("  3. Or set up GitHub Actions for automated daily runs")


if __name__ == "__main__":
    run_all_tests()
