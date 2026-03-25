#!/usr/bin/env python3
import os
import json
import urllib.request
import urllib.error
import subprocess
import sys

os.chdir(r"C:\Users\samruddhi\Desktop\cogni")

USERNAME = "ballisticmessile"
TOKEN = "YOUR_GITHUB_TOKEN_HERE"  # Replace with your personal access token
REPO_NAME = "cogni"

print("[*] Testing GitHub token...")
try:
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github+json"
    }
    
    req = urllib.request.Request(
        "https://api.github.com/user",
        headers=headers,
        method='GET'
    )
    
    with urllib.request.urlopen(req) as response:
        user_data = json.loads(response.read().decode())
        print(f"[✓] Token valid! User: {user_data.get('login', 'N/A')}")
except Exception as e:
    print(f"[✗] Token error: {e}")
    sys.exit(1)

print(f"\n[*] Creating repository '{REPO_NAME}' on GitHub...")
url = "https://api.github.com/user/repos"

data = {
    "name": REPO_NAME,
    "description": "Cogni Quiz Platform - Full-stack quiz application",
    "private": False,
    "auto_init": False
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers=headers,
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode())
        print(f"[✓] Repository created!")
        print(f"    URL: {response_data.get('html_url')}")
except urllib.error.HTTPError as e:
    error_body = e.read().decode()
    if e.code == 422:
        print(f"[!] Repository already exists")
    else:
        print(f"[✗] Error {e.code}: {error_body}")
except Exception as e:
    print(f"[✗] Error: {e}")

# Now push using git
print(f"\n[*] Setting up git executable path...")
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = r"C:\Program Files\Git\bin\git.exe"

from git import Repo

try:
    repo = Repo(".")
    
    print("[*] Configuring git user...")
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", USERNAME)  
        git_config.set_value("user", "email", "ballisticmessile@github.com")
    
    print("[*] Adding files...")
    repo.git.add(A=True)
    
    print("[*] Creating commit...")
    try:
        repo.index.commit("Initial commit: Cogni Quiz Platform")
        print("[✓] Commit created")
    except:
        print("[!] No new changes")
    
    print("[*] Setting up remote...")
    REPO_URL = f"https://{USERNAME}:{TOKEN}@github.com/{USERNAME}/{REPO_NAME}.git"
    try:
        repo.remotes.origin.set_url(REPO_URL)
    except:
        repo.create_remote("origin", REPO_URL)
    
    print("[*] Pushing to GitHub (this may take a moment)...")
    repo.remotes.origin.push(refspec="HEAD:main", force=True)
    
    print(f"\n" + "="*50)
    print(f"[SUCCESS] Project pushed to GitHub!")
    print(f"https://github.com/{USERNAME}/{REPO_NAME}")
    print("="*50)
    
except Exception as e:
    print(f"\n[✗] Push failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
