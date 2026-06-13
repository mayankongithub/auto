#!/bin/bash
# Setup script for cron-based scheduling (alternative to GitHub Actions)

echo "🔧 Setting up Cron Job for Daily Job Search Automation"
echo "========================================================"

# Get the absolute path to the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/job_search_automation.py"
PYTHON_PATH=$(which python3)

# Load environment variables
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file from .env.example and configure your credentials."
    exit 1
fi

# Create a wrapper script that loads environment variables
WRAPPER_SCRIPT="$SCRIPT_DIR/run_job_search.sh"

cat > "$WRAPPER_SCRIPT" << EOF
#!/bin/bash
# Wrapper script to run job search with environment variables

# Load environment variables
export \$(cat "$ENV_FILE" | grep -v '^#' | xargs)

# Change to script directory
cd "$SCRIPT_DIR"

# Run the Python script
$PYTHON_PATH "$PYTHON_SCRIPT" >> "$SCRIPT_DIR/cron_log.txt" 2>&1
EOF

chmod +x "$WRAPPER_SCRIPT"

# Create cron entry (11:00 PM IST = 17:30 UTC, but for local use we'll use local time)
CRON_ENTRY="0 23 * * * $WRAPPER_SCRIPT"

echo ""
echo "📝 Cron entry to be added:"
echo "$CRON_ENTRY"
echo ""
echo "This will run the job search daily at 11:00 PM local time."
echo ""
read -p "Do you want to add this to your crontab? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if entry already exists
    if crontab -l 2>/dev/null | grep -q "$WRAPPER_SCRIPT"; then
        echo "⚠️  Cron entry already exists. Skipping..."
    else
        # Add to crontab
        (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
        echo "✅ Cron job added successfully!"
    fi
    
    echo ""
    echo "📋 Current crontab:"
    crontab -l
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "📌 Notes:"
    echo "  - Logs will be saved to: $SCRIPT_DIR/cron_log.txt"
    echo "  - To view logs: tail -f $SCRIPT_DIR/cron_log.txt"
    echo "  - To remove cron job: crontab -e (then delete the line)"
    echo "  - To test now: $WRAPPER_SCRIPT"
else
    echo "❌ Setup cancelled."
    echo ""
    echo "To add manually later, run:"
    echo "  crontab -e"
    echo "Then add this line:"
    echo "  $CRON_ENTRY"
fi
