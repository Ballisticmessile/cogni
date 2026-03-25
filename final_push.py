#!/usr/bin/env python3
import os
import json
import urllib.request
import urllib.error

os.chdir(r"C:\Users\samruddhi\Desktop\cogni")

# GitHub credentials
USERNAME = "ballisticmessile"
TOKEN = "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"
REPO_NAME = "cogni"

# Set git executable
import platform
if platform.system() == "Windows":
    possible_paths = [
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Program Files (x86)\Git\bin\git.exe",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = path
            break

from git import Repo
from git.exc import GitCommandError

try:
    output = []
    
    # Step 1: Create repository on GitHub
    output.append("[*] Creating repository on GitHub...")
    url = "https://api.github.com/user/repos"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github+json"
    }
    
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
            output.append(f"[✓] Repository created: {response_data.get('html_url', 'N/A')}")
    except urllib.error.HTTPError as e:
        if e.code == 422:  # Already exists
            output.append("[!] Repository already exists on GitHub")
        else:
            output.append(f"[!] GitHub API error: {e.code} - {e.read().decode()}")
    except urllib.error.URLError as e:
        output.append(f"[!] Network error: {e.reason}")
    
    # Step 2: Push to GitHub
    output.append("\n[*] Configuring local repository...")
    repo = Repo(".")
    
    # Configure user
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", USERNAME)
        git_config.set_value("user", "email", "ballisticmessile@github.com")
    output.append("[✓] Git user configured")
    
    # Add all files
    output.append("\n[*] Adding files...")
    repo.git.add(A=True)
    output.append("[✓] Files added")
    
    # Commit
    output.append("\n[*] Creating commit...")
    try:
        repo.index.commit("Initial commit: Cogni Quiz Platform - Full-stack quiz application with user authentication, 20 subjects, admin panel, dark mode, and responsive design")
        output.append("[✓] Commit created")
    except:
        output.append("[!] No new changes to commit")
    
    # Add remote
    output.append("\n[*] Setting up GitHub remote...")
    REPO_URL = f"https://{USERNAME}:{TOKEN}@github.com/{USERNAME}/{REPO_NAME}.git"
    try:
        repo.remotes.origin.set_url(REPO_URL)
        output.append("[✓] Remote updated")
    except:
        repo.create_remote("origin", REPO_URL)
        output.append("[✓] Remote created")
    
    # Push
    output.append("\n[*] Pushing to GitHub...")
    repo.remotes.origin.push(refspec="HEAD:main", force=True)
    output.append("[✓] Successfully pushed to GitHub!")
    
    success_msg = "\n".join(output)
    success_msg += f"\n\n[SUCCESS] Your project is now live at:"
    success_msg += f"\n  https://github.com/{USERNAME}/{REPO_NAME}"
    
    with open("push_success.txt", "w") as f:
        f.write(success_msg)
        
    print("\n".join(output))

except Exception as e:
    error_output = "\n".join(output) if output else ""
    error_output += f"\n\nERROR: {str(e)}\n"
    
    import traceback
    error_output += traceback.format_exc()
    
    with open("push_error.txt", "w") as f:
        f.write(error_output)
    
    print(error_output)
