#!/bin/bash

# Number of fake commits you want to generate
COMMIT_COUNT=50

for ((i=1; i<=COMMIT_COUNT; i++))
do
   # Create an empty commit with a generic message
   git commit --allow-empty -m "Automated commit $i"
done

# Push the commits to your remote repository
git push origin main
