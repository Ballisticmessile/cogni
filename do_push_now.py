#!/usr/bin/env python3
import os
import json
import urllib.request
import urllib.error
import time

os.chdir(r"C:\Users\samruddhi\Desktop\cogni")

USERNAME = "ballisticmessile"
TOKEN = "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"
REPO_NAME = "cogni"

# Set git path
import platform
if platform.system() == "Windows":
    for path in [r"C:\Program Files\Git\bin\git.exe", r"C:\Program Files (x86)\Git\bin\git.exe"]:
        if os.path.exists(path):
            os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = path
            break

from git import Repo

# Create repo on GitHub
print("Creating repository on GitHub...", flush=True)
url = "https://api.github.com/user/repos"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
    "Accept": "application/vnd.github+json"
}
data = {
    "name": REPO_NAME,
    "description": "Cogni Quiz Platform",
    "private": False,
    "auto_init": False
}

try:
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        print("Repository created on GitHub", flush=True)
except urllib.error.HTTPError as e:
    if e.code == 422:
        print("Repository already exists", flush=True)
    else:
        print(f"GitHub error: {e.code}", flush=True)

time.sleep(2)

# Now push
print("Configuring local git...", flush=True)
repo = Repo(".")

with repo.config_writer() as git_config:
    git_config.set_value("user", "name", USERNAME)
    git_config.set_value("user", "email", "ballisticmessile@github.com")

print("Adding files...", flush=True)
repo.git.add(A=True)

print("Creating commit...", flush=True)
try:
    repo.index.commit("Initial commit: Cogni Quiz Platform")
except:
    print("No changes to commit", flush=True)

print("Setting remote...", flush=True)
REPO_URL = f"https://{USERNAME}:{TOKEN}@github.com/{USERNAME}/{REPO_NAME}.git"
try:
    repo.remotes.origin.set_url(REPO_URL)
except:
    repo.create_remote("origin", REPO_URL)

print("Pushing to GitHub...", flush=True)
repo.remotes.origin.push(refspec="HEAD:main", force=True)

print("\nSUCCESS! Project pushed to:", flush=True)
print(f"https://github.com/{USERNAME}/{REPO_NAME}", flush=True)
