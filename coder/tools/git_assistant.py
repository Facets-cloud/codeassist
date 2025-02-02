import subprocess
import os
import logging
from typing import ClassVar

from swarm import Agent


class GitAssistant(Agent):
    base_path: ClassVar[str] = ''

    def __init__(self):
        super().__init__()
        self.name = "Git Assistant"
        self.model: str = "gpt-4o"
        # Read instructions from the Markdown file
        with open('tools/git_assistant.md', 'r') as file:
            self.instructions = file.read()
        self.functions = [
            self.git_status,
            self.git_diff,
            self.git_add,  # Newly added function
            self.git_commit,
            self.git_push,  # Added git push function
            self.git_log,   # List git commits
            self.git_reset, # Unstage changes
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

    def git_add(self, files="."):
        """Executes git add for the specified list of files as strings. If no file is specified, adds all files."""
        if not files or files == '':
            files = "."
        file_list = files.split() if isinstance(files, str) else files
        logging.info(f"Adding {files} to staging area...")
        result = subprocess.run(["git", "add"] + file_list, cwd=self.base_path, capture_output=True, text=True)
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

    def git_log(self, n=10):
        """Lists the latest n git commits."""
        logging.info("Retrieving git log...")
        result = subprocess.run(["git", "log", f"-n {n}"], cwd=self.base_path, capture_output=True, text=True)
        logging.info("Git log retrieved.")
        return result.stdout

    def git_reset(self):
        """Unstages all changes in the current repository."""
        logging.info("Unstaging all changes...")
        result = subprocess.run(["git", "reset"], cwd=self.base_path, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("All changes unstaged.")
        else:
            logging.error("Failed to unstage changes.")
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
