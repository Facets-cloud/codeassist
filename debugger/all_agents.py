from swarm import Agent
import sys

# Removed CodeAssistant import
# Removed GitAssistant import
# Removed ContextAssistant import
from tools.triage_assistant import TriageAssistant
from tools.facets_platform_assistant import FacetsPlatformAssistant

# Removed GitAssistant usage
# Removed ContextAssistant usage
# Removed CodeAssistant usage
triage_agent = TriageAssistant()
facets_assistant = FacetsPlatformAssistant()

if len(sys.argv) < 2:
    print("Error: Base path not provided. Please provide a base path as the first argument.")
    sys.exit(1)

base_path = sys.argv[1]  # The first argument after the script name


def initialize_agents(path):
    print("Base Path: " + path)
    TriageAssistant.base_path = path


initialize_agents(base_path)


# Triage Agent

def transfer_back_to_triage():
    """Transfer the conversation back to the Triage agent."""
    return triage_agent


def transfer_to_facets_assistant():
    """Transfer the conversation to the Facets Platform Assistant."""
    return facets_assistant


# Extend triage_agent functions
triage_agent.functions = [
    transfer_to_facets_assistant
]
facets_assistant.functions.extend([transfer_back_to_triage])
