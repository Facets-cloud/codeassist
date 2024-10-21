from swarm import Agent

from tools.code_assistant import CodeAssistant
from tools.git_assistant import GitAssistant
from tools.triage_assistant import TriageAssistant

git_tool = GitAssistant()
code_tool = CodeAssistant()
triage_tool = TriageAssistant(git_tool, code_tool)


# Triage Agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine which agent is best suited to handle the user's request and transfer the conversation to "
                 "that agent. Important first step is to ask user to, configure the base path for the assistants."
)

# Coding Assistant Agent
agent_coding = Agent(
    name="Coding Assistant",
    instructions=(
        "The Coding Assistant is designed to help users write code efficiently. "
        "It starts by asking the user for the base path for the code. If the user does not provide one, the default is the current directory. "
        "Once the base path is set, the assistant will wait for the user's instructions and, based on the instructions, will list files, read files, or write files to complete the task. "
        "Do not only suggest changes in console but ask user if they want you to edit the files and do that"
        "If there are too many directories or files, the assistant will ask the user for guidance on where to look for the relevant content."
    ),
    functions=[code_tool.list_files,
               code_tool.read_file, code_tool.write_file]
)


# Git Assistant Agent
agent_git = Agent(
    name="Git Assistant",
    instructions=(
        "The Git Assistant is designed to help users manage their Git workflow. "
        "It can perform actions such as checking the status of the repository, crafting commit messages, it can also list the git diff "
        "and executing commits. The agent also updates the requirements.txt with notes on dependencies."
    ),
    functions=[
        git_tool.git_status,
        git_tool.git_diff,
        git_tool.git_commit,
        git_tool.update_requirements
    ]
)


def transfer_to_coding_assistant():
    """Transfer the conversation to the Coding Assistant agent."""
    return agent_coding


def transfer_to_git_assistant():
    """Transfer the conversation to the Coding Assistant agent."""
    return agent_git


def transfer_back_to_triage():
    """Transfer the conversation back to the Triage agent."""
    return triage_agent


# Extend triage_agent functions
triage_agent.functions = [
    triage_tool.set_base_path,
    transfer_to_coding_assistant
]
agent_coding.functions.extend([transfer_back_to_triage, transfer_to_git_assistant])
agent_git.functions.extend([transfer_back_to_triage])
