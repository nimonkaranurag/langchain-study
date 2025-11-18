import unittest
from app.utils.export import export_chat_json, export_chat_markdown
import os

class TestExportFunctions(unittest.TestCase):
    def setUp(self):
        self.chat_history = [
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi, how can I help you?"}
        ]

    def test_export_json(self):
        filename = export_chat_json(self.chat_history, "test_chat.json")
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

    def test_export_markdown(self):
        filename = export_chat_markdown(self.chat_history, "test_chat.md")
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()
