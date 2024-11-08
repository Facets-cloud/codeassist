from tools.config_util import ConfigUtil

class FacetsPlatformAssistant:
    """Assistant for interacting with the Facets platform."""

    def __init__(self):
        self.name = "Facets Platform Assistant"
        self.model = "gpt-4o"
        self.instructions = self.construct_prompt()
        self.functions = []  # Currently no functions defined

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
