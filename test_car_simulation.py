import unittest
from unittest.mock import patch
from io import StringIO
import os

class TestCarSimulation(unittest.TestCase):
    def read_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    def test_scenario1(self):
        input_path = os.path.join("testdata", "scenario1_input.txt")
        expected_path = os.path.join("testdata", "scenario1_expected.txt")

        user_input = self.read_file(input_path)
        expected_output = self.read_file(expected_path)

        # Prepare inputs as a list for side_effect
        input_lines = user_input.strip().splitlines()

        with patch('builtins.input', side_effect=input_lines), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:

            import app  # your script filename without .py
            app.start_menu()

            output = mock_stdout.getvalue()
            print("=== OUTPUT START ===")
            print(output)
            print("=== OUTPUT END ===")
            self.assertIn(expected_output.strip(), output)

if __name__ == "__main__":
    unittest.main()
