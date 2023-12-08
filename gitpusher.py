import os
import time
from github import Github

# Function to push a new file to the GitHub repository
def push_to_github(file_path, repo, branch_name, commit_message):
    with open(file_path, 'r') as file:
        content = file.read()

    repo.create_file(
        path=file_path,
        message=commit_message,
        content=content,
        branch=branch_name
    )

# GitHub credentials
github_token = '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'
github_repo_name = 'smart-breeder-files'
github_repo_owner = 'Birphon'
branch_name = 'main'  # Change this to your main branch name
commit_message = 'Added new file'

# Local folder to watch for new files
folder_to_watch = './downloads'

# Connect to GitHub using PyGithub library
g = Github(github_token)
repo = g.get_user(github_repo_owner).get_repo(github_repo_name)

# Get the list of files in the folder
existing_files = set(os.listdir(folder_to_watch))

while True:
    # Check for new files in the folder
    current_files = set(os.listdir(folder_to_watch))
    new_files = current_files - existing_files

    # If there are new files, push them to the GitHub repository
    if new_files:
        for file_name in new_files:
            file_path = os.path.join(folder_to_watch, file_name)
            push_to_github(file_path, repo, branch_name, commit_message)
            print(f'Pushed {file_name} to GitHub')

        # Update the list of existing files
        existing_files = current_files

    # Add a delay before checking again
    time.sleep(60)  # Check every 60 seconds
