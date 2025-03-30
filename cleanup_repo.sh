#!/bin/bash

# Repository cleanup script
echo "=== ClearBox Repository Cleanup ==="
echo "This script will remove unnecessary files to clean up the repository"
echo ""

# Create a log of what we're going to delete
echo "Creating backup record of deleted files..."
mkdir -p cleanup_logs
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="cleanup_logs/cleanup_${TIMESTAMP}.log"

# List of files to delete (add files here)
echo "Files to be deleted:" | tee -a "$LOG_FILE"
echo "-----------------" | tee -a "$LOG_FILE"

# Redundant build archives
echo "* clearbox/frontend-build.tar.gz (redundant, superseded by frontend-build-update.tar.gz)" | tee -a "$LOG_FILE"
echo "* clearbox/backend-update.tar.gz (already applied to server)" | tee -a "$LOG_FILE"
echo "* clearbox/backend-websocket-update.tar.gz (already applied to server)" | tee -a "$LOG_FILE"
echo "* clearbox/frontend_src_logo_update.tar.gz (already applied to codebase)" | tee -a "$LOG_FILE"
echo "* clearbox/deployment_scripts.tar.gz (scripts already in deploy directory)" | tee -a "$LOG_FILE"

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

# Delete redundant build archives
rm -v clearbox/frontend-build.tar.gz 2>> "$LOG_FILE" | tee -a "$LOG_FILE"
rm -v clearbox/backend-update.tar.gz 2>> "$LOG_FILE" | tee -a "$LOG_FILE"
rm -v clearbox/backend-websocket-update.tar.gz 2>> "$LOG_FILE" | tee -a "$LOG_FILE"
rm -v clearbox/frontend_src_logo_update.tar.gz 2>> "$LOG_FILE" | tee -a "$LOG_FILE"
rm -v clearbox/deployment_scripts.tar.gz 2>> "$LOG_FILE" | tee -a "$LOG_FILE"

# Keep only the latest frontend build archive in deploy-package
echo "* Keeping only the latest frontend build archive in deploy-package" | tee -a "$LOG_FILE"

# Clean up macOS .DS_Store files
echo ""
echo "Removing .DS_Store files..." | tee -a "$LOG_FILE"
find clearbox -name ".DS_Store" -type f -delete -print | tee -a "$LOG_FILE"

echo ""
echo "Cleanup complete!" | tee -a "$LOG_FILE"
echo "A log of the deleted files has been saved to $LOG_FILE"

# Committing the changes
echo ""
read -p "Do you want to commit these changes to git? (y/n): " commit_confirm
if [[ "$commit_confirm" == "y" ]]; then
  echo "Committing changes to git..."
  git add -A
  git commit -m "Clean up repository by removing unnecessary deployment files and archives"
  git push
  echo "Changes committed and pushed successfully!"
else
  echo "Git commit skipped. You can commit the changes manually."
fi 