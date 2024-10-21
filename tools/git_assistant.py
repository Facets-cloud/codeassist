import subprocess
import os
import logging
from typing import ClassVar

from swarm import Agent


PROMPT = """
If a request is not related to operations this agent can do, immediately refer it back to triage for proper handling.
You are the Git Assistant, responsible for managing the current state of the repository. 
Your tasks include checking the current Git status, adding files to the staging area after confirming with the user, 
retrieving the diff of changes,
crafting a meaningful commit message no adjectives to the point and related to output from git diff, confirming it with 
the user, and committing the changes upon approval, and pushing changes to the remote repository when required. 
     
"""


class GitAssistant(Agent):
    base_path: ClassVar[str] = ''

    def __init__(self):
        super().__init__()
        self.name = "Git Assistant"
        self.model: str = "gpt-4o"
        self.instructions = PROMPT
        self.functions = [
            self.git_status,
            self.git_diff,
            self.git_add,  # Newly added function
            self.git_commit,
            self.git_push,  # Added git push function
            self.update_requirements
        ]
        self.tool_choice: str = None
        self.parallel_tool_calls: bool = True


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
        message = message + "\n\n Crafted by Jarvis"
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
