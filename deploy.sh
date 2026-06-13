#!/bin/bash
# Deployment helper script for GitHub setup

echo "============================================================"
echo "🚀 Job Search Automation - Deployment Helper"
echo "============================================================"
echo ""
echo "This will help you deploy to GitHub for daily automation"
echo ""
echo "📋 What we'll do:"
echo "  1. Open GitHub to create a new repository"
echo "  2. Guide you through adding the remote"
echo "  3. Push your code"
echo "  4. Open repository settings for secrets"
echo ""
read -p "Press ENTER to start..."

echo ""
echo "Step 1: Creating GitHub Repository..."
echo "Opening GitHub in your browser..."
sleep 2
open "https://github.com/new"

echo ""
echo "📝 In the browser:"
echo "  - Repository name: job-search-automation"
echo "  - Set to Private (recommended)"
echo "  - DON'T initialize with README"
echo "  - Click 'Create repository'"
echo ""
read -p "Press ENTER after creating the repository..."

echo ""
echo "Step 2: What's your GitHub username?"
read -p "GitHub username: " github_username

echo ""
echo "Adding GitHub remote..."
git remote add origin "https://github.com/$github_username/job-search-automation.git"

echo ""
echo "Step 3: Pushing code to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Code pushed successfully!"
echo ""
echo "Step 4: Setting up GitHub Secrets..."
echo "Opening repository settings..."
sleep 2
open "https://github.com/$github_username/job-search-automation/settings/secrets/actions"

echo ""
echo "📝 Add these secrets:"
echo ""
echo "Secret 1:"
echo "  Name: SERPAPI_KEY"
echo "  Value: 573e565c346fe33e67afda24076ae8f4e9b7ce038f73d6391f8080f547c464f2"
echo ""
echo "Secret 2 (Optional - for email):"
echo "  Name: SENDER_EMAIL"
echo "  Value: mayank0611sharma@gmail.com"
echo ""
echo "Secret 3 (Optional - for email):"
echo "  Name: SENDER_PASSWORD"
echo "  Value: (your Gmail app password)"
echo ""
read -p "Press ENTER after adding secrets..."

echo ""
echo "Step 5: Enabling and testing workflow..."
echo "Opening Actions tab..."
sleep 2
open "https://github.com/$github_username/job-search-automation/actions"

echo ""
echo "📝 In the Actions tab:"
echo "  1. Enable workflows if prompted"
echo "  2. Click 'Daily Job Search Automation'"
echo "  3. Click 'Run workflow' → 'Run workflow'"
echo "  4. Wait for completion (~2-3 minutes)"
echo "  5. Download artifacts to see results"
echo ""
echo "============================================================"
echo "✅ Deployment Complete!"
echo "============================================================"
echo ""
echo "Your job search will now run automatically every day at 11 PM IST!"
echo ""
echo "📊 Monitor runs: https://github.com/$github_username/job-search-automation/actions"
echo "📧 Results: Download artifacts from each run"
echo ""
echo "🎉 Happy job hunting!"
