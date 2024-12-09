import json
import subprocess
import logging
from typing import List

from swarm.types import AgentFunction, Agent


class K8sAssistant(Agent):
    """Assistant for interacting with the Facets platform."""

    def __init__(self):
        super().__init__()
        self.name: str = "Kubernetes Assistant"
        self.model: str = "gpt-4o"
        self.instructions = self.construct_prompt()
        self.functions: List[AgentFunction] = [self.run_kubernetes_command, self.check_cluster_access]
        self.tool_choice: str = None
        self.parallel_tool_calls: bool = True

    def construct_prompt(self):
        prompt = """
"
You are a Kubernetes Debugger Agent designed to diagnose issues in Kubernetes clusters only when explicitly requested by the user. You can execute read-only kubectl commands using run_kubernetes_command(cluster_name, command) and validate access with check_cluster_access(cluster_name). Additionally, you are an expert coder capable of interpreting logs from all types of applications. When fetching logs, you must retrieve them in batches of 1000 lines from the end to ensure optimal performance.

This model's maximum context length is 128,000 tokens, so you should optimize your responses to be efficient, concise, and within this limit while maintaining all necessary details.

Responsibilities:
Cluster Name Validation:
Ensure cluster_name is always provided when requested to diagnose an issue.
Use check_cluster_access(cluster_name) to confirm access before running any commands.
Stop execution and notify the user if access is denied or an issue arises.
Read-Only Commands:
Execute only read-only commands like get, describe, logs, and top.
Ensure no write operations or changes to the cluster state.
Diagnostics:
Run multiple commands to gather detailed insights into resources, logs, events, and metrics.
Interpret logs (retrieved in 1000-line batches from the end) for actionable findings, whether they are application errors, runtime logs, or Kubernetes system logs.
Highlight potential issues such as:
Resource constraints (CPU, Memory).
Misconfigurations or quota issues.
Network or connectivity problems.
Application-level errors or crash reasons.
Workflow:
Prompt for cluster_name if missing and validate access.
Run read-only commands to analyze the issue:
kubectl get pods for an overview of pod statuses.
kubectl describe pod <pod-name> to inspect pod details.
kubectl logs <pod-name> in 1000-line batches to analyze logs.
kubectl get events for recent cluster events.
kubectl top for resource utilization metrics.
Summarize findings, identify issues, and provide solutions or recommendations.
Notify the user if resolving the issue requires write access.
Important:
Do nothing unless explicitly requested by the user.
Provide clear and actionable diagnostics when prompted, ensuring all operations are read-only.
Use the 128,000-token context limit efficiently by avoiding unnecessary verbosity while maintaining clarity and detail.
Notify users of limitations when an issue requires write access.      """
        return prompt

    def _run_command(self, command, directory="."):
        """Run a command using subprocess and return the output."""
        try:
            result = subprocess.run(command, shell=True, cwd=directory, check=True, capture_output=True, text=True)
            logging.info(f"Command '{command}' executed successfully in {directory}.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running command '{command}' in {directory}: {e.stderr}")
            return f"Error running command '{command}' in {directory}: {e.stderr}"

    def run_kubernetes_command(self, cluster_name, command):
        """The command should not include kubectl in it Run a kubectl command on the specified cluster, exporting the KUBECONFIG."""
        # Load configurations
        with open('parameters.json', 'r') as f:
            parameters = json.load(f)
        kubeconfig = parameters['clusters'].get(cluster_name, {}).get('kubeconfig')
        if not kubeconfig:
            raise ValueError(f"Kubeconfig not found for cluster: {cluster_name}")
        # Run command with kubeconfig
        command_to_run = f'KUBECONFIG="{kubeconfig}" kubectl {command}'
        return self._run_command(command_to_run)

    def check_cluster_access(self, cluster_name):
        """Check if the specified cluster exists and if the kubeconfig file has access the returned value is the description of error or success."""
        # Load configurations
        with open('parameters.json', 'r') as f:
            parameters = json.load(f)
        kubeconfig = parameters['clusters'].get(cluster_name, {}).get('kubeconfig')
        if not kubeconfig:
            return f"Cluster '{cluster_name}' does not exist"
        # Run a command to check access
        command_to_run = f'KUBECONFIG="{kubeconfig}" kubectl cluster-info'
        output = self._run_command(command_to_run)
        if output and "Kubernetes master is running at" in output:
            return "Access to cluster successful."
        else:
            return f"{output}"
