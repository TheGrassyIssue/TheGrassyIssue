#!/bin/bash
cd ~/Desktop/TheGrassyIssue/site
git add .
git commit -m "site update $(date '+%b %d %I:%M%p')"
git push
echo ""
echo "✓ Site deployed to thegrassyissue.com"
