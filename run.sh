#!/bin/bash

# Installing dependencies
pip install -r requirements.txt || exit 1

# Go to the "main" directory
cd main || exit 1

# Executing the database_control.py file (creating a database)
python database_control.py || exit 1

# Running app.py and bot.py
python app.py &
python bot.py