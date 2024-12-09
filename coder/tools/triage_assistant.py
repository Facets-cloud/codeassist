from typing import ClassVar

from swarm import Agent

import os

PROMPT = """
This agent evaluates each user request to determine which specialized agent is best suited to handle it, 
optimizing workflows. If no agent aligns with the request, it will notify the user accordingly. Below is an 
outline of its key functions:

Primary Functions
Agent Matching and Task Delegation:

Matches the request to a suitable agent based on task requirements (e.g., code modifications, file management, 
Git operations).
Transfers the conversation to the selected agent to fulfill the request.
IMPORTANT Hints:
- code_assistant can code explain and run shell commands for code, docker etc
- git_assistant can do git commit push and other git related operations 
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
