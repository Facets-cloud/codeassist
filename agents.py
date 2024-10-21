from swarm import Agent
import os

class CodeAssistant:
    def __init__(self):
        self.base_path = ""

    def set_base_path(self, path: str):
        """Set the base path for the agent to operate in."""
        self.base_path = path
        print(f"Base path set to: {self.base_path}")

    def list_files(self, directory: str):
        """List files in a given directory relative to the base path, respecting .gitignore."""
        dir_path = os.path.join(self.base_path, directory)
        if not os.path.exists(dir_path):
            print(f"Directory {dir_path} does not exist.")
            return []

        # Read and parse .gitignore
        gitignore_path = os.path.join(self.base_path, '.gitignore')
        ignore_patterns = []
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as file:
                ignore_patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]

        # List all files and filter out ignored ones
        files = os.listdir(dir_path)
        filtered_files = [f for f in files if not any(os.path.fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns)]

        print(f"Files in {dir_path} (filtered): {filtered_files}")
        return filtered_files

    def read_file(self, file_name_with_path: str):
        """Read the content of a file."""
        file_path = os.path.join(self.base_path, file_name_with_path)
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            print(f"Content of {file_path} read successfully.")
            return content
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return None

    def write_file(self, file_name_with_path: str, content: str):
        """Write content to a file."""
        file_path = os.path.join(self.base_path, file_name_with_path)
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"Content written to {file_path} successfully.")
            return "Success!"
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
            return "Error"

# Coding Assistant Agent
coding_assistant_agent = Agent(
    name="Coding Assistant",
    instructions=(
        "The Coding Assistant is designed to help users write code efficiently. "
        "It starts by asking the user for the base path for the code. If the user does not provide one, the default is the current directory. "
        "Once the base path is set, the assistant will wait for the user's instructions and, based on the instructions, will list files, read files, or write files to complete the task. "
        "Do not only suggest changes in console but ask user if they want you to edit the files and do that"
        "If there are too many directories or files, the assistant will ask the user for guidance on where to look for the relevant content."
    ),
    functions=[CodeAssistant().set_base_path, CodeAssistant().list_files, CodeAssistant().read_file, CodeAssistant().write_file]
)

