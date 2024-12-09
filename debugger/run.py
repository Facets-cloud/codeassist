from swarm.repl import run_demo_loop
from all_agents import triage_agent, k8s_assistant
from swarm import Swarm
import json
import logging
from tools.config_util import ConfigUtil

log_file = 'app.log'  # Specify your log file path

# File handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Get the root logger, set level, clear existing handlers, and add both handlers
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set root logger level to DEBUG to capture all messages
logger.handlers.clear()  # Clear any existing handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def load_parameters():
    """Load parameters using ConfigUtil."""
    return ConfigUtil.load_config()

parameters = load_parameters()
# Expose configuration for agents
CONFIG = parameters.get('facets', {})
# Read model from parameters
MODEL = parameters.get('model', 'gpt-4o-mini')

def process_and_print_streaming_response(response):
    content = ""
    last_sender = ""

    for chunk in response:
        if "sender" in chunk:
            last_sender = chunk["sender"]

        if "content" in chunk and chunk["content"] is not None:
            if not content and last_sender:
                print(f"\033[94m{last_sender}:\033[0m", end=" ", flush=True)
                last_sender = ""
            print(chunk["content"], end="", flush=True)
            content += chunk["content"]

        if "tool_calls" in chunk and chunk["tool_calls"] is not None:
            for tool_call in chunk["tool_calls"]:
                f = tool_call["function"]
                name = f["name"]
                if not name:
                    continue
                print(f"\033[94m{last_sender}: \033[95m{name}\033[0m()")

        if "delim" in chunk and chunk["delim"] == "end" and content:
            print()  # End of response message
            content = ""

        if "response" in chunk:
            return chunk["response"]


def pretty_print_messages(messages) -> None:
    for message in messages:
        if message["role"] != "assistant":
            continue

        # print agent name in blue
        print(f"\033[94m{message['sender']}\033[0m:", end=" ")

        # print response, if any
        if message["content"]:
            print(message["content"])

        # print tool calls in purple, if any
        tool_calls = message.get("tool_calls") or []
        if len(tool_calls) > 1:
            print()
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            print(f"\033[95m{name}\033[0m({arg_str[1:-1]})")


def run_demo_loop(
        starting_agent, context_variables=None, stream=False, debug=False
) -> None:
    client = Swarm()
    print("Starting Swarm CLI 🐝")

    messages = []
    agent = starting_agent

    while True:
        print("\033[90mUser\033[0m: (Enter multiple lines. Press Enter on an empty line to finish)")
        user_input_lines = []

        # Collect multiple lines of input
        while True:
            line = input()  # Takes input from the user line by line
            if line == "":  # Stop when the user presses Enter on an empty line
                break
            user_input_lines.append(line)

        user_input = "\n".join(user_input_lines)  # Combine the lines into a single string
        messages.append({"role": "user", "content": user_input})

        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
            stream=stream,
            model_override=MODEL,
            debug=debug,
        )

        if stream:
            response = process_and_print_streaming_response(response)
        else:
            pretty_print_messages(response.messages)

        messages.extend(response.messages)
        agent = response.agent

if __name__ == "__main__":
    run_demo_loop(k8s_assistant)