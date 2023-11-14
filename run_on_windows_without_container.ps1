# Installing dependencies
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { exit 1 }

# Go to the "main" directory
cd main
if ($LASTEXITCODE -ne 0) { exit 1 }

# Executing the build_project.py file
python build_project.py
if ($LASTEXITCODE -ne 0) { exit 1 }

# Running app.py and bot.py
Start-Process python -ArgumentList "app.py" -NoNewWindow
Start-Process python -ArgumentList "bot.py" -NoNewWindow
