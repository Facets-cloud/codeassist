# Project README

Welcome to the Swarm-based AI Coding Assistant! This application leverages capabilities from the Swarm project to provide a multi-agent coding assistant designed to streamline development tasks.

## Overview

This project develops an AI agent to assist with coding tasks, utilizing a triage system to distribute tasks among specialized agents. The application is fundamentally based on the [Swarm Project](https://github.com/openai/swarm.git).

## Getting Started

### Prerequisites

Ensure you have Python installed on your machine. You'll also need to clone the repository and install the necessary dependencies. You can typically do this with:

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
pip install -r requirements.txt
```

### Running the Application

The primary interface for interacting with the coding assistant is through the command line. To start the application, run:

```bash
python run.py /path/to/your/code
```

**Note**: Replace `/path/to/your/code` with the actual file path where your project or codebase resides. This allows the coding assistant to interact appropriately with your files.

## Usage Guide

Upon starting, follow the on-screen prompts:

1. **Input Commands**: Enter your queries or tasks, pressing Enter after each line, and use a blank line to submit.
2. **Interactive Responses**: The CLI will process inputs using the appropriate agents and display results inline.
3. **Agent Transfers**: Tasks can seamlessly move between agents (e.g., coding, git, context) as decided by the triage logic.

### Capabilities

- **Code Assistance**: Receive suggestions on code completion, error checking, and refactoring through the coding assistant.
- **Version Control**: Leverage the git assistant for committing, pushing, and managing code versions.
- **Contextual Help**: The context assistant can provide file details to better understand code structures and purposes.

## Logging

All actions and interactions are logged to `app.log`. This file is generated in the application directory and is useful for debugging and tracking activity.

## Contributing

Feel free to submit issues, request features, or contribute to the codebase by submitting a pull request.

## License

This project is licensed under the MIT License.
