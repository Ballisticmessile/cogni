#!/usr/bin/env python3
import subprocess
import os
import sys

os.chdir(r'C:\Users\samruddhi\Desktop\cogni')

# Try different git paths
git_paths = [
    r'C:\Program Files\Git\bin\git.exe',
    r'C:\Program Files (x86)\Git\bin\git.exe',
    'git'
]

for git_exe in git_paths:
    try:
        result = subprocess.run([git_exe, '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            with open(r'C:\git_check.txt', 'w') as f:
                f.write(f"Found Git: {git_exe}\n")
                f.write(f"Version: {result.stdout}\n")
                
                # Check status
                status = subprocess.run([git_exe, 'status'], capture_output=True, text=True)
                f.write(f"\nGit Status:\n{status.stdout}\n")
                
                # Check remote
                remote = subprocess.run([git_exe, 'remote', '-v'], capture_output=True, text=True)
                f.write(f"\nRemotes:\n{remote.stdout}\n")
                
                #Check log
                log = subprocess.run([git_exe, 'log', '--oneline', '-5'], capture_output=True, text=True)
                f.write(f"\nCommits:\n{log.stdout}\n")
            break
    except:
        pass
else:
    with open(r'C:\git_check.txt', 'w') as f:
        f.write("Git not found\n")

print("Results written to C:\\git_check.txt")
