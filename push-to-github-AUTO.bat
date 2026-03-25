@echo off
REM Cogni Quiz Platform - GitHub Push Script with Token
REM This script automatically pushes your project to GitHub

setlocal enabledelayedexpansion

set USERNAME=ballisticmessile
set TOKEN=YOUR_GITHUB_TOKEN_HERE REM Replace with your personal access token
set REPO_URL=https://%USERNAME%:%TOKEN%@github.com/%USERNAME%/cogni.git

cd /d C:\Users\samruddhi\Desktop\cogni

echo ========================================
echo   Cogni - Pushing to GitHub
echo ========================================
echo.

REM Configure git
echo [1/5] Configuring Git...
"C:\Program Files\Git\bin\git.exe" config --global user.email "ballisticmessile@github.com"
"C:\Program Files\Git\bin\git.exe" config --global user.name "ballisticmessile"
echo ✓ Git configured

REM Initialize repository
echo [2/5] Initializing Git repository...
if exist .git (
  echo ✓ Repository already exists
) else (
  "C:\Program Files\Git\bin\git.exe" init
  echo ✓ Repository initialized
)

REM Add files
echo [3/5] Adding files...
"C:\Program Files\Git\bin\git.exe" add .
echo ✓ Files added

REM Create commit
echo [4/5] Creating commit...
"C:\Program Files\Git\bin\git.exe" commit -m "Initial commit: Cogni Quiz Platform - Full-stack quiz application with user authentication, 20 subjects, admin panel, dark mode, and responsive design"
echo ✓ Commit created

REM Configure remote
echo [5/5] Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" remote remove origin 2>nul
"C:\Program Files\Git\bin\git.exe" remote add origin %REPO_URL%
"C:\Program Files\Git\bin\git.exe" branch -M main

REM Push
"C:\Program Files\Git\bin\git.exe" push -u origin main

if errorlevel 1 (
  echo.
  echo ❌ Error during push!
  echo Make sure your token is valid and try again.
) else (
  echo.
  echo ✅ SUCCESS! Your project is now on GitHub!
  echo Repository: https://github.com/%USERNAME%/cogni
)

echo.
pause
