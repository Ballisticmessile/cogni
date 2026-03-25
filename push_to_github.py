#!/usr/bin/env python3
import subprocess
import os
import sys

# Configuration
USERNAME = "ballisticmessile"
TOKEN = "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"
REPO_URL = f"https://{USERNAME}:{TOKEN}@github.com/{USERNAME}/cogni.git"
PROJECT_DIR = r"C:\Users\samruddhi\Desktop\cogni"

# Change to project directory
os.chdir(PROJECT_DIR)
print(f"Working directory: {os.getcwd()}")

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n[★] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ERROR: {result.stderr}")
            if result.stdout:
                print(f"OUTPUT: {result.stdout}")
            return False
        else:
            if result.stdout:
                print(result.stdout)
            return True
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

# Find git executable
git_locations = [
    "git",  # Try PATH first
    r"C:\Program Files\Git\bin\git.exe",
    r"C:\Program Files (x86)\Git\bin\git.exe",
]

git_exe = None
for location in git_locations:
    try:
        result = subprocess.run(f'"{location}" --version', shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            git_exe = location
            print(f"✓ Found Git: {location}")
            print(f"  Version: {result.stdout.strip()}")
            break
    except:
        pass

if not git_exe:
    print("✗ Git not found! Please install Git from https://git-scm.com/download/win")
    sys.exit(1)

# Build git command with full path
def git(args):
    return f'"{git_exe}" {args}'

print("\n" + "="*50)
print("  Cogni - Pushing to GitHub")
print("="*50)

# Step 1: Configure Git
run_command(git('config --global user.email "ballisticmessile@github.com"'), "Configuring Git email")
run_command(git('config --global user.name "ballisticmessile"'), "Configuring Git name")

# Step 2: Initialize repository
if os.path.exists(".git"):
    print("\n[★] Repository already exists")
else:
    run_command(git('init'), "Initializing Git repository")

# Step 3: Add files
run_command(git('add .'), "Adding files to git")

# Step 4: Create commit
commit_msg = "Initial commit: Cogni Quiz Platform - Full-stack quiz application with user authentication, 20 subjects, admin panel, dark mode, and responsive design"
run_command(git(f'commit -m "{commit_msg}"'), "Creating commit")

# Step 5: Configure remote
run_command(git('remote remove origin'), "Removing old remote (if exists)")
run_command(git(f'remote add origin {REPO_URL}'), "Adding GitHub remote")

# Step 6: Set main branch
run_command(git('branch -M main'), "Setting main as default branch")

# Step 7: Push to GitHub
push_success = run_command(git('push -u origin main'), "Pushing to GitHub")

print("\n" + "="*50)
if push_success:
    print("✓ SUCCESS! Your project is now on GitHub!")
    print(f"  Repository: https://github.com/{USERNAME}/cogni")
else:
    print("✗ Push failed. Check your token and internet connection.")
print("="*50)
