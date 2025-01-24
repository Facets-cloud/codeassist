import unittest
import os
from tools.code_assistant import CodeAssistant

class TestCodeAssistant(unittest.TestCase):
    def setUp(self):
        """Create a temporary file for testing."""
        self.test_file_path = 'test_file.txt'
        self.test_content = "Line 1\nLine 2\nLine 3\n"
        with open(self.test_file_path, 'w') as f:
            f.write(self.test_content)
        
        self.code_assistant = CodeAssistant()

    def tearDown(self):
        """Remove the temporary file after tests."""
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_apply_diff_to_file(self):
        """Test applying diffs to a file."""
        # Prepare a unified diff to update Line 2 and add a new line
        diff = """--- test_file.txt\n+++ test_file.txt\n@@ -1,3 +1,4 @@\n Line 1\n-Line 2\n+Line 2 Updated\n Line 3\n+Line 4\n"""
        result = self.code_assistant.apply_diff_to_file(self.test_file_path, diff)
        
        with open(self.test_file_path, 'r') as f:
            updated_content = f.read()
        
        expected_content = "Line 1\nLine 2 Updated\nLine 3\nLine 4\n"
        
        self.assertEqual(result, "Success!")
        self.assertEqual(updated_content, expected_content)

if __name__ == '__main__':
    unittest.main()
