import os
import fnmatch
import re
from typing import List, ClassVar
import subprocess
import yaml  # Import the yaml module
import logging

from swarm import Agent
from swarm.types import AgentFunction

PROMPT = """
Coding Assistant Functionality Overview
This Coding Assistant is designed to assist users with tasks related to explaining, writing, and editing code within their codebase. It offers robust file management, code operations, and collaborative editing capabilities, ensuring precision and efficiency for specific coding instructions.

Agent Capabilities
Code Explanation and Modification:
Provides clear explanations for code and updates it as per user instructions.

File Management:
Lists, searches, and manages files or directories to help focus on specific areas of the project.

Code Operations:
Reads, edits, and finds content within files, making various code modifications with a focus on precision.

Shell Command Execution:
Executes shell commands and provides output, enabling users to leverage system commands for advanced tasks.

Coding Assistant Tools and Functions
File Management:

list_files: Lists all files or directories within the project. For large lists, the assistant will prompt the user to specify where to focus.
find_file: Searches for files by name or pattern, allowing precise file access.
Code Operations:

read_file: Reads and retrieves the content of a specified file.
write_file: Creates or updates a file with new or modified content.
Important: Always ensure existing content is not overwritten unintentionally. Read, edit, and write operations must maintain the integrity of prior content unless explicitly instructed otherwise.
find_string_in_files: Searches for specific strings or patterns across multiple files to locate files of interest or relevant code segments.
create_directory: Creates a directory if it does not exist.
Shell Command Execution:

run_shell_command: Executes shell commands, providing output to enhance productivity and access to system-level tasks.
Collaborative Editing:

Suggests code changes based on user instructions and confirms them with the user before applying. Uses write_file to implement changes after validation.
Version Control:

All version control-related tasks are delegated to the git_assistant, ensuring seamless integration with Git workflows.
Key Guidelines
Always ensure no content is skipped or lost while performing file edits.
Use a workflow of read → modify → write to safeguard the integrity of the original file content unless explicitly instructed otherwise.
Maintain clear and concise communication with users, ensuring that suggestions are confirmed before changes are applied.
"""


class CodeAssistant(Agent):
    base_path: ClassVar[str] = ''

    def __init__(self):
        super().__init__()
        self.name: str = "Coder"
        self.model: str = "gpt-4o"
        self.instructions = self.construct_prompt_with_context()
        self.functions: List[AgentFunction] = [self.list_files,
                                               self.read_file,
                                               self.write_file,
                                               self.find_string_in_files, self.find_file,
                                               self.create_directory, self.run_shell_command]
        self.tool_choice: str = None
        self.parallel_tool_calls: bool = True

    def construct_prompt_with_context(self):
        project_context = self.read_context_file_as_string()
        new_prompt = PROMPT + "\n\nProject file contexts:\n" + project_context
        return new_prompt

    def list_files(self, directory: str):
        """List files in a given directory relative to the base path, respecting .gitignore."""
        dir_path = os.path.join(self.base_path, directory)
        if not os.path.exists(dir_path):
            logging.warning(f"Directory {dir_path} does not exist.")
            return []

        # Read and parse .gitignore
        gitignore_path = os.path.join(self.base_path, '../../.gitignore')
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

    def find_file(self, file_pattern: str, dir_path: str = ".", use_regex: bool = False):
        """Find a file by name or regex pattern within the directory path, respecting .gitignore."""
        dir_path = os.path.join(self.base_path, dir_path)
        logging.info(f"Searching for file pattern '{file_pattern}' under {dir_path}...")
        found_files = []

        # Read and parse .gitignore
        gitignore_path = os.path.join(self.base_path, '../../.gitignore')
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
            return "Error"

    def run_shell_command(self, command: str, directory: str):
        """Run a shell command in a specified directory and return its output."""
        directory = os.path.join(self.base_path, directory)
        try:
            result = subprocess.run(command, shell=True, cwd=directory, check=True, capture_output=True, text=True)
            logging.info(f"Command '{command}' executed successfully in {directory}.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running command '{command}' in {directory}: {e.stderr}")
            return None
