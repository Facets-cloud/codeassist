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
        result = subprocess.run(["git", "status"], cwd=self.base_path, capture_output=True, text=True)
        return result.stdout

    def git_diff(self):
        """Runs git diff and returns the output."""
        result = subprocess.run(["git", "diff", "--cached"], cwd=self.base_path, capture_output=True, text=True)
        return result.stdout

    def git_commit(self, message):
        """Executes git commit using the provided message."""
        subprocess.run(["git", "add", "."], cwd=self.base_path)
        result = subprocess.run(["git", "commit", "-m", message], cwd=self.base_path, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr

    def update_requirements(self):
        """Updates requirements.txt with necessary packages for the assistant."""
        reqs_path = os.path.join(self.base_path, "../requirements.txt")
        with open(reqs_path, 'a') as file:
            file.write("\n# Added for Git Assistant\n")
            # Assuming no new external requirements are needed beyond standard lib
            file.write("# No new packages required\n")
