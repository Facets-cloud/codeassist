from swarm import Agent
import sys

from tools.code_assistant import CodeAssistant
from tools.git_assistant import GitAssistant
from tools.triage_assistant import TriageAssistant
from tools.context_assistant import ContextAssistant

git_agent = GitAssistant()
code_agent = CodeAssistant()
triage_agent = TriageAssistant()
context_agent = ContextAssistant()

if len(sys.argv) < 2:
    print("Error: Base path not provided. Please provide a base path as the first argument.")
    sys.exit(1)

base_path = sys.argv[1]  # The first argument after the script name


def initialize_agents(path):
    GitAssistant.base_path = path
    CodeAssistant.base_path = path
    TriageAssistant.base_path = path


initialize_agents(base_path)


# Triage Agen


def transfer_to_coding_assistant():
    """Transfer the conversation to the Coding Assistant agent."""
    return code_agent


def transfer_to_git_assistant():
    """Transfer the conversation to the Coding Assistant agent."""
    return git_agent


def transfer_to_context_assistant():
    """Transfer the conversation to the Coding Assistant agent."""
    return context_agent


def transfer_back_to_triage():
    """Transfer the conversation back to the Triage agent."""
    return triage_agent


# Extend triage_agent functions
triage_agent.functions = [
    transfer_to_coding_assistant
]
code_agent.functions.extend([transfer_back_to_triage, transfer_to_git_assistant])
git_agent.functions.extend([transfer_back_to_triage, transfer_to_context_assistant])
context_agent.functions.extend([transfer_to_git_assistant])
