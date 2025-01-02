from swarm.repl import run_demo_loop
from all_agents import triage_agent
from all_agents import facets_agent
from all_agents import code_agent
from all_agents import git_agent  # Import Git agent
from swarm import Swarm
import json
import logging
import time
import sys

log_file = 'app.log'  # Specify your log file path

def setup_logging():
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
    
    return logger  # Return the logger

def load_parameters():
    with open('parameters.json') as f:
        parameters = json.load(f)
    return parameters.get('model', 'gpt-4o-mini')

# Setup logging
logger = setup_logging()  # Store the logger instance

# Log the model being used
model_override = load_parameters()
logger.info(f'Model being used: {model_override}')

# Print the model being used
print(f'\033[92mModel being used: {model_override}\033[0m')

def process_and_print_streaming_response(response):
    content = ""
    last_sender = ""

    for chunk in response:
        if "sender" in chunk:
            last_sender = chunk["sender"]

        if "content" in chunk and chunk["content"] is not None:
            if not content and last_sender:
                print(f"\n\033[94m{last_sender}:\033[0m", end=" ", flush=True)
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
        print(f"\n\033[94m{message['sender']}\033[0m:", end=" ")

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
        starting_agent, context_variables=None, stream=True, debug=False
) -> None:
    client = Swarm()
    print("\033[92mStarting Swarm CLI 🐝\033[0m")

    messages = []
    agent = starting_agent

    while True:
        print("\033[90mUser\033[0m: (Enter multiple lines. Press Enter on an empty line to finish or type \"/switch agent\" to change agent or \"/\" to change agents using aliases)")
        user_input_lines = []

        # Collect multiple lines of input
        while True:
            line = input()  # Takes input from the user line by line
            if line == "":  # Stop when the user presses Enter on an empty line
                break
            user_input_lines.append(line)

        user_input = "\n".join(user_input_lines)  # Combine the lines into a single string

        # Check if the user wants to switch agents
        if user_input.strip().lower() == "switch agent":
            print("\033[93mSwitching agent...\033[0m")
            return  # Exit the loop and return control to the main function

        # Check if the user wants to use an alias
        if user_input.startswith("/"):
            alias = user_input.replace("/", "").strip()
            if alias in agent_aliases:
                print(f"\033[93mSwitching to agent: {alias}\033[0m")
                agent = agent_aliases[alias]
                continue
            else:
                print("\033[91mInvalid alias! Please try again.\033[0m")

        messages.append({"role": "user", "content": user_input})

        print("\033[96mWaiting for response...\033[0m", end="", flush=True)
        for _ in range(3):  # Simple loading indicator
            print(".", end="", flush=True)
            time.sleep(0.5)
        print()  # New line after loading indicator

        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
            stream=stream,
            model_override=model_override,
            debug=debug,
        )

        if stream:
            response = process_and_print_streaming_response(response)
        else:
            pretty_print_messages(response.messages)

        messages.extend(response.messages)
        agent = response.agent  # Update to the new agent after response


if __name__ == "__main__":
    # Prompt user to select an agent
    agents = {
        "1": code_agent,
        "2": triage_agent,
        "3": facets_agent,
        "4": git_agent  # Added Git agent to the options
    }

    agent_aliases = {
        'code': code_agent,
        'triage': triage_agent,
        'facets': facets_agent,
        'git': git_agent
    }

    print("\033[1m\033[92mWelcome to the Swarm CLI!\033[0m\n")
    while True:
        print("\033[1mSelect an agent to interact with:\033[0m")
        for key in agents.keys():
          alias = [k for k, v in agent_aliases.items() if v == agents[key]]
          print(f"\033[93m{key}:\033[0m {agents[key].name} (/{', '.join(alias)})" if alias else f"\033[93m{key}:\033[0m {agents[key].name}")
        print("\033[90m0: Exit\033[0m")

        selected_agent = input("Enter the number of the agent you want to use or type an alias: ")
        if selected_agent == "0":
            print("\033[92mExiting the agent selection.\033[0m")
            break
        elif selected_agent in agents:
            run_demo_loop(agents[selected_agent])
        elif selected_agent in agent_aliases:
            run_demo_loop(agent_aliases[selected_agent])
        else:
            print("\033[91mInvalid selection! Please try again.\033[0m")
