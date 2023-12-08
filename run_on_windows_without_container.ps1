# Installing dependencies
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { exit 1 }

# Go to the "app" directory
cd app
if ($LASTEXITCODE -ne 0) { exit 1 }

# Executing the build_project.py file
python build_project.py
if ($LASTEXITCODE -ne 0) { exit 1 }

# Running webapp.py and bot.py
Start-Process python -ArgumentList "webapp.py" -NoNewWindow
Start-Process python -ArgumentList "bot.py" -NoNewWindow
