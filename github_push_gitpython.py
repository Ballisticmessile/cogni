#!/usr/bin/env python3
"""
GitHub Push Script using GitPython
No need for git command line tool
"""

try:
    from git import Repo
    from git.exc import GitCommandError, InvalidGitRepositoryError
    import os
    import sys
    
    print("=" * 50)
    print("  Cogni - Pushing to GitHub (Python Git)")
    print("=" * 50)
    
    PROJECT_DIR = r"C:\Users\samruddhi\Desktop\cogni"
    USERNAME = "ballisticmessile"
    TOKEN = "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"
    REPO_URL = f"https://{USERNAME}:{TOKEN}@github.com/{USERNAME}/cogni.git"
    
    os.chdir(PROJECT_DIR)
    print(f"\n[*] Working directory: {PROJECT_DIR}")
    
    # Initialize or get repository
    try:
        print("[*] Opening existing repository...")
        repo = Repo(PROJECT_DIR)
    except InvalidGitRepositoryError:
        print("[*] Initializing new repository...")
        repo = Repo.init(PROJECT_DIR)
    
    print(f"[✓] Repository ready")
    
    # Configure Git
    print("\n[*] Configuring Git...")
    with repo.config_writer() as git_config:
        git_config.set_value("user", "email", "ballisticmessile@gmail.com")
        git_config.set_value("user", "name", "ballisticmessile")
    print("[✓] Git configured")
    
    # Add files
    print("\n[*] Adding files...")
    repo.git.add(A=True)
    print(f"[✓] Files added")
    
    # Check if there are changes to commit
    if repo.is_dirty(untracked_files=True):
        print("\n[*] Creating commit...")
        repo.index.commit("Initial commit: Cogni Quiz Platform - Full-stack quiz application with user authentication, 20 subjects, admin panel, dark mode, and responsive design")
        print("[✓] Commit created")
    else:
        print("\n[*] No changes to commit (repository already up to date)")
    
    # Setup remote
    print("\n[*] Setting up GitHub remote...")
    try:
        repo.remote('origin').set_url(REPO_URL)
        print("[✓] Remote updated")
    except:
        repo.create_remote('origin',  REPO_URL)
        print("[✓] Remote created")
    
    # Push to GitHub
    print("\n[*] Pushing to GitHub...")
    try:
        origin = repo.remote('origin')
        origin.push(refspec='HEAD:main', force=True)
        print("[✓] Successfully pushed to GitHub!")
        print(f"\n[SUCCESS] Your project is now live at:")
        print(f"  https://github.com/{USERNAME}/cogni")
    except GitCommandError as e:
        print(f"[✗] Push failed: {e}")
        print("\nNote: If the error mentions 'fatal: HttpRequestException'")
        print("it could be due to network issues or invalid token.")
        sys.exit(1)
    except Exception as e:
        print(f"[✗] Error: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)
    
except ImportError as e:
    print(f"Error: GitPython not installed: {e}")
    print("Run: pip install GitPython")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
