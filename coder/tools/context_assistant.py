import os
import yaml  # Import the yaml module
import logging

from tools.code_assistant import CodeAssistant

class ContextAssistant(CodeAssistant):
    
    def __init__(self):
        super().__init__()
        self.name: str = "Context Assistant"
        self.model: str = "gpt-4o"
        # Read instructions from the Markdown file
        with open('tools/context_assistant.md', 'r') as file:
            self.instructions = file.read()
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