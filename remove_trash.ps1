Remove-Item -Path ".\logs" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\.pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue

cd app
Remove-Item -Path ".\logs" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue

cd ..
cd tests
Remove-Item -Path ".\logs" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\.pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
