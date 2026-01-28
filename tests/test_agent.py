import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory to the sys.path to allow importing agent.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestAgent(unittest.TestCase):

    @patch('agent.subprocess.run')
    @patch('agent.os.getenv')
    @patch('agent.notify_meta_agent_results')
    @patch('agent.generate_pdf')
    @patch('agent.generate_csv')
    def test_agent_script_runs_without_error(self, mock_generate_csv, mock_generate_pdf, mock_notify, mock_getenv, mock_subprocess_run):
        # Mock environment variables
        mock_getenv.side_effect = lambda key: {
            "TELEGRAM_BOT_TOKEN": "test_token",
            "TELEGRAM_CHAT_ID": "test_chat_id"
        }.get(key)

        # Mock subprocess.run for game_ai
        mock_subprocess_run.side_effect = [
            MagicMock(stdout="Final Digits : ['1', '2']\nSafe Jodis   : ['12', '21']", stderr="", returncode=0),
            MagicMock(stdout="Hot Digit (Jodi): 3\nSupport Jodis: 34, 43", stderr="", returncode=0)
        ]

        # Ensure the script runs without raising an exception
        try:
            import agent
            # Call the main execution block
            agent.main() # Assuming the main execution logic is wrapped in a function called main()
        except Exception as e:
            self.fail(f"agent.py raised an exception: {e}")

        # Assert that subprocess.run was called for both game_ai and jodi
        self.assertEqual(mock_subprocess_run.call_count, 2)
        
        # Assert that PDF and CSV reports were generated
        mock_generate_pdf.assert_called_once()
        mock_generate_csv.assert_called_once()

        # Assert that Telegram notification was attempted
        mock_notify.assert_called_once()

if __name__ == '__main__':
    unittest.main()
