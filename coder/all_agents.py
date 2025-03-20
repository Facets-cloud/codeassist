from swarm import Agent
import sys

from tools.code_assistant import CodeAssistant
from tools.facets_assistant import FacetsAssistant
from tools.git_assistant import GitAssistant
from tools.triage_assistant import TriageAssistant
from tools.context_assistant import ContextAssistant
from tools.cliassistant import CLIAssistant

git_agent = GitAssistant()
code_agent = CodeAssistant('Coder')
swagger_agent = CodeAssistant('Swagger', 'tools/code_swagger_gen.md')
swagger_agent_2 = CodeAssistant('Permission Agent', 'tools/permission_agent.md')

architect = CodeAssistant('Explainer', 'tools/code_explainer.md')
triage_agent = TriageAssistant()
context_agent = ContextAssistant()
facets_agent = FacetsAssistant()
cli_agent = CLIAssistant()


def transfer_to_permission_agent():
    """Transfer the conversation to the Permission agent."""
    return swagger_agent_2


swagger_agent.functions.extend([transfer_to_permission_agent])


def transfer_to_apidoc_agent():
    """Transfer the conversation to the APIDocAgent agent."""
    return swagger_agent


swagger_agent_2.functions.extend([transfer_to_apidoc_agent])

if len(sys.argv) < 2:
    print("Error: Base path not provided. Please provide a base path as the first argument.")
    sys.exit(1)

base_path = sys.argv[1]  # The first argument after the script name


def initialize_agents(path):
    print("Base Path: " + path)
    GitAssistant.base_path = path
    CodeAssistant.base_path = path
    TriageAssistant.base_path = path
    FacetsAssistant.base_path = path


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
    transfer_to_coding_assistant,
    transfer_to_git_assistant,
    transfer_to_context_assistant
]
git_agent.functions.extend([transfer_to_context_assistant])
context_agent.functions.extend([transfer_to_git_assistant])
