# tools/base_assistant.py

class BaseAssistant:
    def __init__(self):
        self.context = {}
    
    def fulfill_inputs(self, prompt):
        """Prompts for additional input and appends it to the context."""
        user_input = input(prompt)
        self.append_to_context(user_input)
    
    def append_to_context(self, input_data):
        """Appends the provided input data to the context."""
        if isinstance(input_data, str) and input_data:
            self.context.setdefault('additional_info', []).append(input_data)
        elif isinstance(input_data, dict):
            self.context.update(input_data)
        # Further handling of context data can be done here.