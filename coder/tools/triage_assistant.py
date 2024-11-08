from typing import ClassVar

from swarm import Agent

import os

PROMPT = """
Determine which agent is best suited to handle the user's request and transfer the conversation to 
that agent. It integrates and coordinates the capabilities of other agents, managing base paths 
and optimizing workflows across the system.
        """


# Configure logging
class TriageAssistant(Agent):
    base_path: ClassVar[str] = ''
    def __init__(self):
        super().__init__()
        self.name = "Triage Agent"
        self.instructions = self.construct_prompt_with_context()
        self.functions = []
        self.tool_choice: str = None
        self.parallel_tool_calls: bool = True
        self.model: str = "gpt-4o"

    def load_project_context(self):
        context_file = os.path.join(self.base_path, 'project_context.txt')
        if os.path.exists(context_file):
            with open(context_file, 'r') as file:
                return file.read()
        return ''

    def construct_prompt_with_context(self):
        project_context = self.load_project_context()
        return PROMPT + "\n\nProject context specified by user:\n" + project_context
