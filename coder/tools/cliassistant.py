import os
import subprocess
import platform
import logging
from swarm import Agent
from typing import List, ClassVar
from swarm.types import AgentFunction


class CLIAssistant(Agent):
    base_path: ClassVar[str] = ''

    def __init__(self):
        super().__init__()
        self.name: str = "CLI Runner"
        self.model: str = "gpt-4o"
        # Read instructions from the Markdown file
        with open('tools/cli_assistant.md', 'r') as file:
            self.instructions = file.read()
        self.functions: List[AgentFunction] = [self.run_shell_command]
        self.tool_choice: str = None
        self.parallel_tool_calls: bool = True

    def run_shell_command(self, command: str, directory: str):
        """Run a shell command in a specified directory and stream its output in real-time, returning the full output."""
        directory = os.path.join(self.base_path, directory)

        # Check the current operating system
        os_name = platform.system()
        logging.info(f"Operating System: {os_name}")

        output_lines = []  # Store the command output

        try:
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # Stream output line by line and store it
            for line in iter(process.stdout.readline, ''):
                logging.info(line.strip())  # Log output
                output_lines.append(line.strip())  # Store output

            process.stdout.close()
            return_code = process.wait()

            if return_code != 0:
                logging.error(f"Command '{command}' failed with exit code {return_code}")

            return "\n".join(output_lines)  # Return full output as a string

        except Exception as e:
            logging.error(f"Exception running command '{command}' in {directory}: {e}")
            return str(e)
