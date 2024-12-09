from swarm import Agent
import sys

# Removed CodeAssistant import
# Removed GitAssistant import
# Removed ContextAssistant import
from tools.triage_assistant import TriageAssistant
from tools.k8s_assistant import K8sAssistant

# Removed GitAssistant usage
# Removed ContextAssistant usage
# Removed CodeAssistant usage
triage_agent = TriageAssistant()
k8s_assistant = K8sAssistant()


# Triage Agent

def transfer_back_to_triage():
    """Transfer the conversation back to the Triage agent."""
    return triage_agent


def transfer_to_facets_assistant():
    """Transfer the conversation to the Kubernetes Assistant."""
    return k8s_assistant


# Extend triage_agent functions
triage_agent.functions = [
    transfer_to_facets_assistant
]
k8s_assistant.functions.extend([transfer_back_to_triage])
