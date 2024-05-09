#!/bin/env sh

git config --global user.email "none"

git config --global user.name "none"

git clone https://github.com/MothScientist/BudgetGraph.git

git checkout master

# Time and date of test build
current_datetime=$(date +'%H_%M__%d-%m-%Y')

# Random number to avoid duplicate assembly names
random_number=$(head -200 /dev/urandom | cksum | cut -c 1-5)

git checkout -b build_"$current_datetime"_"$random_number"

git add .

git commit -m "GitHubActions_Git_'$current_datetime'_'$random_number'"

if git merge master; then
    echo "> Status: SUCCESS"
    exit 0
else
    git merge --abort
    echo "> Status: ERROR"
    echo ">> Check the error message after 'git merge' command"
    exit 1
fi
