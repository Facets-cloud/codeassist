import os
import fnmatch
import yaml  # Import the yaml module
import logging

class CodeAssistant:
    def __init__(self):
        self.base_path = ""

    def set_base_path(self, path: str):
        """Set the base path for the agent to operate in."""
        self.base_path = path
        logging.info(f"Base path set to: {self.base_path}")

    def list_files(self, directory: str):
        """List files in a given directory relative to the base path, respecting .gitignore."""
        dir_path = os.path.join(self.base_path, directory)
        if not os.path.exists(dir_path):
            logging.warning(f"Directory {dir_path} does not exist.")
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

        logging.info(f"Files in {dir_path} (filtered): {filtered_files}")
        return filtered_files

    def read_file(self, file_name_with_path: str):
        """Read the content of a file."""
        file_path = os.path.join(self.base_path, file_name_with_path)
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            logging.info(f"Content of {file_path} read successfully.")
            return content
        except FileNotFoundError:
            logging.error(f"File {file_path} not found.")
            return None
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            return None

    def write_file(self, file_name_with_path: str, content: str):
        """Write content to a file."""
        file_path = os.path.join(self.base_path, file_name_with_path)
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            logging.info(f"Content written to {file_path} successfully.")
            return "Success!"
        except Exception as e:
            logging.error(f"Error writing to {file_path}: {e}")
            return "Error"

    def find_string_in_files(self, search_string: str, dir_path: str = None):
        """Search for a string in all files within the directory path, respecting .gitignore."""
        dir_path = dir_path or self.base_path
        logging.info(f"Searching for '{search_string}' in files under {dir_path}...")
        matched_files = []

        # Read and parse .gitignore
        gitignore_path = os.path.join(self.base_path, '../.gitignore')
        ignore_patterns = []
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as file:
                ignore_patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]

        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Skip ignored files
                if any(fnmatch.fnmatch(file_path, pattern) for pattern in ignore_patterns):
                    continue
                try:
                    with open(file_path, 'r') as f:
                        if search_string in f.read():
                            matched_files.append(file_path)
                            logging.info(f"String found in {file_path}")
                except Exception as e:
                    logging.error(f"Error reading {file_path}: {e}")

        logging.info(f"Search completed. Files matched: {matched_files}")
        return matched_files

    def read_context_file(self):
        """Read and parse the context.yml file, returning its content as a dictionary."""
        content = self.read_file('context.yml')
        logging.info("Reading context.yml content.")
        if content:
            return yaml.safe_load(content) or {}
        return {}

    def update_context_file(self, file_path: str, context_content: str):
        """Add or update file context in the context.yml file."""
        context_file_path = os.path.join(self.base_path, 'context.yml')

        # Load existing contexts using the read_context_file method
        context_data = self.read_context_file()

        # Update context
        context_data[file_path] = context_content

        # Write updated context back to the file using the write_file method
        success = self.write_file('context.yml', yaml.safe_dump(context_data, default_flow_style=False))

        if success:
            logging.info(f"Context for {file_path} updated in {context_file_path}")
        else:
            logging.error(f"Failed to update context for {file_path} in {context_file_path}")
