from swarm import Agent
import os
import fnmatch  # Import the fnmatch module

class CodeAssistant:
    def __init__(self):
        self.base_path = ""

    def set_base_path(self, path: str):
        """Set the base path for the agent to operate in."""
        self.base_path = path
        print(f"Base path set to: {self.base_path}")

    def list_files(self, directory: str):
        """List files in a given directory relative to the base path, respecting .gitignore."""
        dir_path = os.path.join(self.base_path, directory)
        if not os.path.exists(dir_path):
            print(f"Directory {dir_path} does not exist.")
            return []

        # Read and parse .gitignore
        gitignore_path = os.path.join(self.base_path, '../.gitignore')
        ignore_patterns = []
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as file:
                ignore_patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]

        # List all files and filter out ignored ones
        files = os.listdir(dir_path)
        filtered_files = [f for f in files if not any(fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns)]

        print(f"Files in {dir_path} (filtered): {filtered_files}")
        return filtered_files

    def read_file(self, file_name_with_path: str):
        """Read the content of a file."""
        file_path = os.path.join(self.base_path, file_name_with_path)
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            print(f"Content of {file_path} read successfully.")
            return content
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return None

    def write_file(self, file_name_with_path: str, content: str):
        """Write content to a file."""
        file_path = os.path.join(self.base_path, file_name_with_path)
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"Content written to {file_path} successfully.")
            return "Success!"
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
            return "Error"

    def find_string_in_files(self, search_string: str, dir_path: str = None):
        """Search for a string in all files within the directory path."""
        dir_path = dir_path or self.base_path
        print(f"Searching for '{search_string}' in files under {dir_path}...")
        matched_files = []

        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        if search_string in f.read():
                            matched_files.append(file_path)
                            print(f"String found in {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

        return matched_files
