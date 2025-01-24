from typing import ClassVar

from swarm import Agent

import os

class TriageAssistant(Agent):
    base_path: ClassVar[str] = ''

    def __init__(self):
        super().__init__()
        self.name = "Triage Agent"
        # Read instructions from the Markdown file
        with open('tools/triage_assistant.md', 'r') as file:
            self.instructions = file.read()
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
        return self.instructions + "\n\nProject context specified by user:\n" + project_context
