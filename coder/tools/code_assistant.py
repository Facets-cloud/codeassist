import os
import fnmatch
import re
from typing import List, ClassVar
import subprocess
import yaml  # Import the yaml module
import logging
from unidiff import PatchSet

from swarm import Agent
from swarm.types import AgentFunction

class CodeAssistant(Agent):
    base_path: ClassVar[str] = ''
    
    def __init__(self):
        super().__init__()
        self.name: str = "Coder"
        self.model: str = "gpt-4o"
        # Read instructions from the Markdown file
        with open('tools/code_assistant.md', 'r') as file:
            self.instructions = file.read()
        self.functions: List[AgentFunction] = [self.list_files,
                                               self.read_file,
                                               self.write_file,
                                               self.find_string_in_files, self.find_file,
                                               self.create_directory,
                                               self.run_shell_command
                                               ]  
        self.tool_choice: str = None
        self.parallel_tool_calls: bool = True

    def _validate_file_path(self, file_name_with_path: str):
        """Validate that the file path does not start with '../'."""
        if file_name_with_path.startswith("../"):
            logging.error(f"Invalid file path: {file_name_with_path}. Path cannot start with '../'.")
            return False
        return True

    def _validate_directory_path(self, dir_path: str):
        """Validate that the directory path does not start with '../'."""
        if dir_path.startswith("../"):
            logging.error(f"Invalid directory path: {dir_path}. Path cannot start with '../'.")
            return False
        return True
    
    def list_files(self, directory: str, gitignore_path: str = None):
        """List files in a given directory relative to the base path, respecting the specified .gitignore file."""
        dir_path = os.path.join(self.base_path, directory)
        if not os.path.exists(dir_path):
            logging.warning(f"Directory {dir_path} does not exist.")
            return []
        ignore_patterns = []
        if gitignore_path and os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as file:
                ignore_patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        
        # List all files and filter out ignored ones
        files = os.listdir(dir_path)
        filtered_files = [f for f in files if not any(fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns)]
        
        logging.info(f"Files in {dir_path} (filtered): {filtered_files}")
        return filtered_files
    
    def read_file(self, file_name_with_path: str):
        """Read the content of a specified file, ensuring the path is valid and not starting with '../'."""
        file_path = os.path.join(self.base_path, file_name_with_path)

        logging.info(f"Content of {file_path} ")

        if not self._validate_file_path(file_name_with_path):
            return "Invalid file path. Path cannot start with '../'."
        
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            logging.info(f"Content of {file_path} read successfully.")
            return content
        except FileNotFoundError:
            logging.error(f"File {file_path} not found.")
            return f"File {file_path} not found."
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            return str(e)
    
    def write_file(self, file_name_with_path: str, content: str):
        """Write specified content to a file, ensuring the path is valid and not starting with '../'."""
        if not self._validate_file_path(file_name_with_path):
            return "Invalid file path. Path cannot start with '../'."
        
        file_path = os.path.join(self.base_path, file_name_with_path)
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            logging.info(f"Content written to {file_path} successfully.")
            return "Success!"
        except Exception as e:
            logging.error(f"Error writing to {file_path}: {e}")
            return str(e)

    def append_to_file(self, file_name_with_path: str, content: str):
        """Append content to a file."""
        file_path = os.path.join(self.base_path, file_name_with_path)
        try:
            with open(file_path, 'a') as file:
                file.write(content)
            logging.info(f"Content appended to {file_path} successfully.")
            return "Success!"
        except Exception as e:
            logging.error(f"Error appending to {file_path}: {e}")
            return "Error"

    def find_string_in_files(self, search_string: str, dir_path: str, file_pattern: str = '*'):
        """Search for a string within the directory path, respecting the file pattern and limiting to 1000 results."""
        dir_path = os.path.join(self.base_path, dir_path)
        logging.info(f"Searching for '{search_string}' in files matching '{file_pattern}' under {dir_path}...")

        # Construct the grep command with include pattern and limiting output
        grep_command = f"grep -rl --include='{file_pattern}' '{search_string}' {dir_path}"

        try:
            # Run the grep command
            process = subprocess.run(grep_command, shell=True, check=True, capture_output=True, text=True)

            # Process the output and limit to 1000 results
            matched_files = process.stdout.splitlines()[:1000]

            for match in matched_files:
                logging.info(f"String found: {match}")

            logging.info(f"Search completed. Matches found: {len(matched_files)}")
            return matched_files

        except subprocess.CalledProcessError as e:
            logging.error(f"Error running grep command: {e.stderr}")
            return []

    def read_context_file_as_string(self):
        """Read and parse the context.yml file, returning its content as a dictionary."""
        content = self.read_file('context.yml')
        logging.info("Reading context.yml content.")
        return content

    def find_file(self, file_pattern: str, dir_path: str = ".", use_regex: bool = False, gitignore_path: str = None):
        """Find a file by name or regex pattern within the specified directory, respecting the specified .gitignore file."""
        if not self._validate_directory_path(dir_path):
            return "Invalid directory path. Path cannot start with '../'."
        
        dir_path = os.path.join(self.base_path, dir_path)
        logging.info(f"Searching for file pattern '{file_pattern}' under {dir_path}...")
        found_files = []
        
        # Read and parse .gitignore
        ignore_patterns = []
        if gitignore_path and os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as file:
                ignore_patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Skip ignored files
                if any(fnmatch.fnmatch(file_path, pattern) for pattern in ignore_patterns):
                    continue
                # Match using regex or fnmatch
                if use_regex:
                    if re.search(file_pattern, file):
                        found_files.append(file_path)
                        logging.info(f"File found: {file_path}")
                else:
                    if fnmatch.fnmatch(file, file_pattern):
                        found_files.append(file_path)
                        logging.info(f"File found: {file_path}")
        
        logging.info(f"Search completed. Files found: {found_files}")
        return found_files
    
    def create_directory(self, dir_name: str):
        """Create a directory if it does not exist."""
        dir_path = os.path.join(self.base_path, dir_name)
        try:
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Directory {dir_path} created successfully.")
            return "Success!"
        except Exception as e:
            logging.error(f"Error creating directory {dir_path}: {e}")
            return str(e)
    
    def run_shell_command(self, command: str, directory: str):
        """Run a shell command in a specified directory and return its output."""
        directory = os.path.join(self.base_path, directory)
        try:
            result = subprocess.run(command, shell=True, cwd=directory, check=True, capture_output=True, text=True)
            logging.info(f"Command '{command}' executed successfully in {directory}.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running command '{command}' in {directory}: {e.stderr}")
            return str(e.stderr)
    
    def apply_diff_to_file(self, file_path: str, diff: str):
        """Apply unified diff to a file using unidiff."""
        try:
            # Read the original file content
            with open(file_path, 'r') as file:
                original_content = file.readlines()
            
            # Create a patch set
            patch = PatchSet(diff)
            
            # Apply the patch
            for p in patch:
                for h in p:
                    for line in h:
                        if line.is_added:
                            original_content.insert(line.target_line_no - 1, line.value)
                        elif line.is_removed:
                            del original_content[line.source_line_no - 1]
            
            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.writelines(original_content)
            
            logging.info(f"Multiple diffs applied to {file_path} successfully.")
            return "Success!"
        except Exception as e:
            logging.error(f"Error applying diffs to {file_path}: {e}")
            return str(e)