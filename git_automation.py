#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3
import os
import subprocess
import sys

def git_init(folder_path):
    os.chdir(folder_path)
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        subprocess.run(["git", "init"], check=True)

def git_remote_exists():
    try:
        subprocess.run(["git", "remote", "get-url", "origin"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        return False

def git_add_commit_push(github_repo_url, folder_path, commit_message):
    os.chdir(folder_path)
    subprocess.run(["git", "status"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)

    if not git_remote_exists():
        subprocess.run(["git", "remote", "add", "origin", github_repo_url], check=True)

    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python git_automation.py <github_repo_url> <folder_path> <commit_message>")
        sys.exit(1)

    github_repo_url = sys.argv[1]
    folder_path = sys.argv[2]
    commit_message = sys.argv[3]

    git_init(folder_path)
    git_add_commit_push(github_repo_url, folder_path, commit_message)
