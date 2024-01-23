#!/bin/env sh

# Go to the "app" directory
cd app || exit 1

# Running webapp.py and bot.py
python webapp.py &
python bot.py