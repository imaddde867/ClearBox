#!/bin/bash

# Additional repository cleanup script
echo "=== ClearBox Repository Advanced Cleanup ==="
echo "This script will remove additional unnecessary files to optimize the repository"
echo ""

# Create a log of what we're going to delete
echo "Creating backup record of deleted files..."
mkdir -p cleanup_logs
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="cleanup_logs/advanced_cleanup_${TIMESTAMP}.log"

# List of files to delete (add files here)
echo "Files and directories to be removed:" | tee -a "$LOG_FILE"
echo "-----------------------------------" | tee -a "$LOG_FILE"

# Python cache files
echo "1. Python __pycache__ directories" | tee -a "$LOG_FILE"
echo "   - These are bytecode cache files that are recreated when needed" | tee -a "$LOG_FILE"

# Pytest cache directory
echo "2. .pytest_cache directory" | tee -a "$LOG_FILE"
echo "   - This is a test cache directory that can be safely removed" | tee -a "$LOG_FILE"

# Build directories that are recreated during build process
echo "3. frontend/build directory (if backup exists in deploy-package)" | tee -a "$LOG_FILE"
echo "   - The build is already backed up in deploy-package/build and deploy-package/.tar.gz" | tee -a "$LOG_FILE"

# Ask for confirmation before proceeding
echo ""
read -p "Are you sure you want to delete these files? (y/n): " confirm
if [[ "$confirm" != "y" ]]; then
  echo "Operation cancelled."
  exit 0
fi

# Delete the files
echo ""
echo "Deleting files..." | tee -a "$LOG_FILE"

# 1. Remove Python __pycache__ directories (but not in venv)
echo "Removing Python __pycache__ directories (excluding venv)..." | tee -a "$LOG_FILE"
find clearbox/backend -name "__pycache__" -type d | grep -v "venv" | xargs rm -rf 2>> "$LOG_FILE" | tee -a "$LOG_FILE"

# 2. Remove .pytest_cache directory
echo "Removing .pytest_cache directory..." | tee -a "$LOG_FILE"
rm -rf clearbox/backend/.pytest_cache 2>> "$LOG_FILE" | tee -a "$LOG_FILE"

# 3. Check if we should remove the frontend/build directory
if [ -d "clearbox/deploy-package/build" ] && [ -f "clearbox/deploy-package/clearbox-frontend-deployment.tar.gz" ]; then
  echo "Removing redundant frontend/build directory (backup exists in deploy-package)..." | tee -a "$LOG_FILE"
  rm -rf clearbox/frontend/build 2>> "$LOG_FILE" | tee -a "$LOG_FILE"
  # Create a placeholder file explaining where the build is
  mkdir -p clearbox/frontend/build
  echo "# Build Directory" > clearbox/frontend/build/README.md
  echo "The production build has been moved to the deploy-package directory for deployment." >> clearbox/frontend/build/README.md
  echo "Run 'npm run build' to regenerate this directory locally." >> clearbox/frontend/build/README.md
else
  echo "Keeping frontend/build directory as no backup was found in deploy-package" | tee -a "$LOG_FILE"
fi

# Add .gitignore rules to prevent future caching issues
echo "Updating .gitignore rules..." | tee -a "$LOG_FILE"
cat << 'EOF' >> clearbox/.gitignore

# Additional ignores from cleanup
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
frontend/build/*
!frontend/build/README.md
.DS_Store
*.log
EOF

echo ""
echo "Cleanup complete!" | tee -a "$LOG_FILE"
echo "A log of the deleted files has been saved to $LOG_FILE"

# Calculating space saved
echo ""
echo "Space savings summary:"
echo "---------------------"
du -sh clearbox
echo ""
echo "Note: Significant space is still used by frontend/node_modules ($(du -sh clearbox/frontend/node_modules | cut -f1)) and backend/venv ($(du -sh clearbox/backend/venv | cut -f1))"
echo "These directories are ignored by git and only exist locally, so they don't affect the repository size."

# Committing the changes
echo ""
read -p "Do you want to commit these changes to git? (y/n): " commit_confirm
if [[ "$commit_confirm" == "y" ]]; then
  echo "Committing changes to git..."
  git add -A
  git commit -m "Advanced cleanup: Remove Python cache files and optimize build directories"
  git push
  echo "Changes committed and pushed successfully!"
else
  echo "Git commit skipped. You can commit the changes manually."
fi 