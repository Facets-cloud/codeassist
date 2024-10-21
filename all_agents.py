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
                 "that agent. It integrates and coordinates the capabilities of other agents, managing base paths "
                 "and optimizing workflows across the system. Important first step is to ask user to configure the "
                 "base path for the assistants."
)

# Coding Assistant Agent
agent_coding = Agent(
    name="Coding Assistant",
    instructions=(
        "The Coding Assistant is designed to help users write and edit code efficiently. It interacts with files in the codebase, "
        "searches for specific content, and assists with reading, writing, and modifying files. "
        "When the agent is invoked first of all Use `read_context_file` to gather information about files and their structure to build context. [Important] Then first use this as primary information to cater to user requests"
        "2. File management: Use `list_files` to offer a list of files or directories when necessary. If there are too many files, ask the user for guidance on where to focus. "
        "3. Code operations: Based on the user's instructions, perform the following tasks: "
        "- Use read_context_file output to determine relevant files"
        "- Use `read_file` to retrieve content. "
        "- Use `write_file` to create or update content. "
        "- Use `find_string_in_files` to locate patterns or specific strings. "
        "4. Collaborative edits: After suggesting code changes, ask the user if they want the file edited directly. If confirmed, use `write_file` to apply the changes. "
        "5. Contextual updates: Use `update_context_file` to maintain what is being done in the file. If the user types 'update context', immediately trigger `update_context_file` to refresh the context. "
        "6. Git operations: For any version control operations, transfer to the `git_assistant`."
    ),
    functions=[
        code_tool.list_files,
        code_tool.read_file,
        code_tool.write_file,
        code_tool.find_string_in_files,
        code_tool.read_context_file,
        code_tool.update_context_file
    ]
)

# Git Assistant Agent
agent_git = Agent(
    name="Git Assistant",
    instructions=(
        "If a request is not related to Git operations, immediately refer it back to triage for proper handling."
        "You are the Git Assistant, responsible for managing the current state of the repository. "
        "Your tasks include checking the current Git status, adding files to the staging area after confirming with the user, retrieving the diff of changes, "
        "crafting a meaningful commit message no adjectives to the point and related to output from git diff, confirming it with the user, and committing the changes upon approval, and pushing changes to the remote repository when required. "
    ),
    functions=[
        git_tool.git_status,
        git_tool.git_diff,
        git_tool.git_add,  # Newly added function
        git_tool.git_commit,
        git_tool.git_push,  # Added git push function
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
