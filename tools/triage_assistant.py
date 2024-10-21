from typing import ClassVar

from swarm import Agent

from tools.code_assistant import CodeAssistant
from tools.git_assistant import GitAssistant
import logging

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
        self.instructions = PROMPT
        self.functions = []
        self.tool_choice: str = None
        self.parallel_tool_calls: bool = True
        self.model: str = "gpt-4o"

