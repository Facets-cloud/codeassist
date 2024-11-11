from tools.config_util import ConfigUtil
import json
import os

class FacetsPlatformAssistant:
    """Assistant for interacting with the Facets platform."""

    def __init__(self):
        self.name = "Facets Platform Assistant"
        self.model = self.load_model()  # Load model from parameters.json
        self.instructions = self.construct_prompt()
        self.functions = []  # Currently no functions defined

    def load_model(self):
        """Load the model from parameters.json."""
        config_file_path = 'parameters.json'  # Specify the path to your parameters.json file
        if not os.path.exists(config_file_path):
            raise FileNotFoundError("parameters.json file not found.")
        with open(config_file_path, 'r') as f:
            parameters = json.load(f)
        return parameters.get('model', 'default_model')  # Provide a default model if not found

    def construct_prompt(self):
        prompt = """
        The Facets Platform Assistant is designed to help users interact with the Facets platform. 
        When this agent is invoked, it will assist users with various operations and facilitate communications within the platform.
        Currently, it does not have any defined functions but is prepared for future enhancements.
        """
        return prompt

    def read_config(self):
        """Read configuration values for the Facets platform."""
        config = ConfigUtil.load_config()
        return {'url': config.get('url'), 'username': config.get('username'), 'token': config.get('token')}

    def fetch_kubeconfig(self, local_directory='./'):
        """Fetch kubeconfig file and save it in a local directory."""
        kubeconfig_url = f"{self.read_config().get('url')}/kubeconfig"
        kubeconfig_path = os.path.join(local_directory, 'kubeconfig')
        try:
            response = requests.get(kubeconfig_url)
            response.raise_for_status()  # Raise an error for bad responses
            with open(kubeconfig_path, 'wb') as f:
                f.write(response.content)
            return kubeconfig_path  # Return the path of the saved kubeconfig
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch kubeconfig: {e}")
            return None
