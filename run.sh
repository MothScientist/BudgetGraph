#!/bin/env sh

# Go to the "main" directory
cd main || exit 1

# Running app.py and bot.py
python app.py &
python bot.py