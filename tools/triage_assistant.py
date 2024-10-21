from tools.code_assistant import CodeAssistant
from tools.git_assistant import GitAssistant
import logging

# Configure logging
class TriageAssistant:

    def __init__(self):
        self.base_path = ""

    def set_base_path(self, path: str):
        """Set the base path for the agent to operate in."""
        self.base_path = path
        logging.info(f"Base path set to: {self.base_path}")

    def set_base_path(self, path: str):
        """Takes a string, Set the base path for the agent to operate in."""
        self.base_path = path
        logging.info(f"Base path set to: {self.base_path} for Triage")

    def get_base_path(self, base_path):
        """Return the base path of the context."""
        logging.info(f"Returning base path: {self.base_path}")
        return self.base_path
