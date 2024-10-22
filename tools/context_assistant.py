import os
import yaml  # Import the yaml module
import logging
from typing import ClassVar

from swarm import Agent

from tools.code_assistant import CodeAssistant

PROMPT = """
The Context Assistant is designed to manage context within the codebase. It focuses on operations related to reading and updating context information stored in files.

You will receive list of files and you have to add them to the context using below instructions. After doing your job transfer back to git assistant without confirming with user and ask it to add files to staging area as asked by user including context.yml
Important: Context should be information about what that file is doing in general not related to particular commit. Make it such that it is easy to understand for other developers.

Use `read_context_file` to gather and parse context data. Use `update_context_file` to add or modify context information.
"""


class ContextAssistant(CodeAssistant):

    def __init__(self):
        super().__init__()
        self.name: str = "Context Assistant"
        self.model: str = "gpt-4o"
        self.instructions = PROMPT
        self.functions = [self.read_context_file,
                          self.update_context_file, self.read_file, self.write_file, self.list_files]

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
