import subprocess
import os
import logging
from swarm import Agent

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GitAssistant:

    def __init__(self):
        self.base_path = ""

    def set_base_path(self, path: str):
        """Set the base path for the agent to operate in."""
        self.base_path = path
        logging.info(f"Base path set to: {self.base_path}")

    def git_status(self):
        """Runs git status and returns the output."""
        logging.info("Checking git status...")
        result = subprocess.run(["git", "status"], cwd=self.base_path, capture_output=True, text=True)
        logging.info("Git status checked.")
        return result.stdout

    def git_diff(self):
        """Runs git diff and returns the output."""
        logging.info("Retrieving git diff...")
        result = subprocess.run(["git", "diff", "--cached"], cwd=self.base_path, capture_output=True, text=True)
        logging.info("Git diff retrieved.")
        return result.stdout

    def git_commit(self, message):
        """Executes git commit using the provided message."""
        message = message + "\n crafted by Jarvis"
        logging.info("Adding files to staging area...")
        subprocess.run(["git", "add", "."], cwd=self.base_path)
        logging.info("Committing changes...")
        result = subprocess.run(["git", "commit", "-m", message], cwd=self.base_path, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("Changes committed.")
        else:
            logging.error("Failed to commit changes.")
        return result.stdout if result.returncode == 0 else result.stderr

    def git_add(self, files=[]):
        """Executes git add for the specified list of files as strings. If no file is specified, adds all files."""
        if not files or files == '':
            files = "."
        logging.info(f"Adding {files} to staging area...")
        result = subprocess.run(["git", "add", files], cwd=self.base_path, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Added {files} to staging area.")
        else:
            logging.error(f"Failed to add {files}.")
        return result.stdout if result.returncode == 0 else result.stderr

    def git_push(self):
        """Executes git push """
        logging.info("Pushing changes to remote repository...")
        result = subprocess.run(["git", "push"], cwd=self.base_path, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("Changes pushed successfully.")
        else:
            logging.error("Failed to push changes.")
        return result.stdout if result.returncode == 0 else result.stderr

    def update_requirements(self):
        """Updates requirements.txt with necessary packages for the assistant."""
        logging.info("Updating requirements.txt...")
        reqs_path = os.path.join(self.base_path, "../requirements.txt")
        with open(reqs_path, 'a') as file:
            file.write("\n# Added for Git Assistant\n")
            # Assuming no new external requirements are needed beyond standard lib
            file.write("# No new packages required\n")
        logging.info("requirements.txt updated.")
