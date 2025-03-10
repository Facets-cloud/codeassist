from swarm import Agent
import sys

from tools.code_assistant import CodeAssistant

writer_agent = CodeAssistant('Facets Modules', 'tools/facets_modules/prompts/module_writer.md')
yaml_agent = CodeAssistant('Facets YAML', 'tools/facets_modules/prompts/facets_yaml.md')
refactor_agent = CodeAssistant('Facets Refactor Agent', 'tools/facets_modules/prompts/refactor_agent.md')


def transfer_to_agent2_Facets_YAML_agent():
    """Transfer the conversation to the Facets YAML agent."""
    return yaml_agent


writer_agent.functions.extend([transfer_to_agent2_Facets_YAML_agent])


def transfer_to_agent3_Refactor_agent():
    """Transfer the conversation to the Facets Refactor agent."""
    return refactor_agent


yaml_agent.functions.extend([transfer_to_agent3_Refactor_agent])
