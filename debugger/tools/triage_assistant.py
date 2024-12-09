from typing import ClassVar

from swarm import Agent

import os

PROMPT = """
Determine which agent is best suited to handle the user's request and transfer the conversation to 
that agent. It integrates and coordinates the capabilities of other agents, managing base paths 
and optimizing workflows across the system. It will only transfer and not answer any other request by the user.
        """


# Configure logging
class TriageAssistant(Agent):
    def __init__(self):
        super().__init__()
        self.name = "Triage Agent"
        self.instructions = self.construct_prompt_with_context()
        self.functions = []
        self.tool_choice: str = None
        self.parallel_tool_calls: bool = True

    def construct_prompt_with_context(self):
        return PROMPT
