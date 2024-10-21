import subprocess
import os
from swarm import Agent


class GitAssistant:

    def __init__(self):
        self.base_path = ""

    def set_base_path(self, path: str):
        """Set the base path for the agent to operate in."""
        self.base_path = path
        print(f"Base path set to: {self.base_path}")

    def git_status(self):
        """Runs git status and returns the output."""
        print("Checking git status...")
        result = subprocess.run(["git", "status"], cwd=self.base_path, capture_output=True, text=True)
        print("Git status checked.")
        return result.stdout

    def git_diff(self):
        """Runs git diff and returns the output."""
        print("Retrieving git diff...")
        result = subprocess.run(["git", "diff", "--cached"], cwd=self.base_path, capture_output=True, text=True)
        print("Git diff retrieved.")
        return result.stdout

    def git_commit(self, message):
        """Executes git commit using the provided message."""
        message = message + "\n crafted by Jarvis"
        print("Adding files to staging area...")
        subprocess.run(["git", "add", "."], cwd=self.base_path)
        print("Committing changes...")
        result = subprocess.run(["git", "commit", "-m", message], cwd=self.base_path, capture_output=True, text=True)
        if result.returncode == 0:
            print("Changes committed.")
        else:
            print("Failed to commit changes.")
        return result.stdout if result.returncode == 0 else result.stderr

    def git_add(self, files=[]):
        """Executes git add for the specified list of files as strings. If no file is specified, adds all files."""
        if not files or files == '':
            files = "."
        print(f"Adding {files} to staging area...")
        result = subprocess.run(["git", "add", files], cwd=self.base_path, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Added {files} to staging area.")
        else:
            print(f"Failed to add {files}.")
        return result.stdout if result.returncode == 0 else result.stderr

    def git_push(self):
        """Executes git push """
        print("Pushing changes to remote repository...")
        result = subprocess.run(["git", "push"], cwd=self.base_path, capture_output=True, text=True)
        if result.returncode == 0:
            print("Changes pushed successfully.")
        else:
            print("Failed to push changes.")
        return result.stdout if result.returncode == 0 else result.stderr

    def update_requirements(self):
        """Updates requirements.txt with necessary packages for the assistant."""
        print("Updating requirements.txt...")
        reqs_path = os.path.join(self.base_path, "../requirements.txt")
        with open(reqs_path, 'a') as file:
            file.write("\n# Added for Git Assistant\n")
            # Assuming no new external requirements are needed beyond standard lib
            file.write("# No new packages required\n")
        print("requirements.txt updated.")
