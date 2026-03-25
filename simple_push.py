#!/usr/bin/env python3
import os
os.chdir(r"C:\Users\samruddhi\Desktop\cogni")

# Find and set git executable
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
    repo = Repo(".")
    
    # Configure user
    repo.config_writer().set_value("user", "name", "ballisticmessile").release()
    repo.config_writer().set_value("user", "email", "ballisticmessile@github.com").release()
    
    # Add all files
    repo.git.add(A=True)
    
    # Commit
    try:
        repo.index.commit("Initial commit: Cogni Quiz Platform")
        commit_msg = "Commit created\n"
    except:
        commit_msg = "No new commit needed\n"
    
    # Add remote
    try:
        repo.remotes.origin.set_url("https://ballisticmessile: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@github.com/ballisticmessile/cogni.git")
    except:
        repo.create_remote("origin", "https://ballisticmessile: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@github.com/ballisticmessile/cogni.git")
    
    # Push
    repo.remotes.origin.push(refspec="HEAD:main", force=True)
    
    with open("push_success.txt", "w") as f:
        f.write("SUCCESS:\n")
        f.write(commit_msg)
        f.write("Repository pushed to GitHub!\n")
        f.write("https://github.com/ballisticmessile/cogni\n")

except Exception as e:
    with open("push_error.txt", "w") as f:
        f.write(f"ERROR: {str(e)}\n")
        import traceback
        f.write(traceback.format_exc())
