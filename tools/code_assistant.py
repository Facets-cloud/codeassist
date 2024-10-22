import os
import fnmatch
from typing import List, ClassVar

import yaml  # Import the yaml module
import logging

from swarm import Agent
from swarm.types import AgentFunction

PROMPT = """
The Coding Assistant is designed to help users write and edit code. It interacts with files in the codebase. 
When the agent is invoked, first use `read_context_file` to gather information about files and their structure to build context. [Important] Then, use this as primary information to cater to user requests.

1. File management: Use `list_files` to offer a list of files or directories when necessary. If there are too many files, ask the user for guidance on where to focus.
2. Code operations: Based on the user's instructions, perform the following tasks:
   - Use `read_file` to retrieve content.
   - Use `write_file` to create or update content.
   - Use `find_string_in_files` to locate patterns or specific strings.
   - When you have context about a file, use `update_context_file` to update the context about what is being done in the file for later use.
3. Collaborative edits: After suggesting code changes, ask the user if they want the file edited directly. If confirmed, use `write_file` to apply the changes.
4. Git operations: For any version control operations, transfer to the `git_assistant`.
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
                                               self.find_string_in_files]
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

    def read_context_file_as_string(self):
        """Read and parse the context.yml file, returning its content as a dictionary."""
        content = self.read_file('context.yml')
        logging.info("Reading context.yml content.")
        return content
