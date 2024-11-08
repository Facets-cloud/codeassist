import json
import os

class ConfigUtil:
    """Utility class to handle configuration reading."""

    @staticmethod
    def load_config(file_path='parameters.json'):
        """Load parameters from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                parameters = json.load(f)
                return parameters.get('facets', {})
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
