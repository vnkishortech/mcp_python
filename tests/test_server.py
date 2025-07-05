import unittest
from mcp_server.server import MCPServer

class TestMCPServer(unittest.TestCase):
    def setUp(self):
        self.server = MCPServer()

    def test_search_papers_returns_list(self):
        # This test will fail if arxiv is not mocked and no internet connection
        result = self.server.search_papers("quantum computing", 1)
        self.assertIsInstance(result, list)

    def test_extract_info_returns_string(self):
        result = self.server.extract_info("nonexistent_id")
        self.assertIsInstance(result, str)

if __name__ == "__main__":
    unittest.main()
