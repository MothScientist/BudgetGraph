# Installing dependencies
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { exit 1 }

# Go to the "main" directory
cd main
if ($LASTEXITCODE -ne 0) { exit 1 }

# Executing the creating_db_and_directories.py file
python creating_db_and_directories.py
if ($LASTEXITCODE -ne 0) { exit 1 }

# Running app.py and bot.py
Start-Process python -ArgumentList "app.py" -NoNewWindow
Start-Process python -ArgumentList "bot.py" -NoNewWindow
