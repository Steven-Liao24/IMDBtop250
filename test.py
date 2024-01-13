import unittest
from unittest.mock import patch
from chatgpymodel import query_openai, split_text
from UI import get_first_text

class TestApp(unittest.TestCase):
    
    def test_split_text(self):
        # Test split_text function
        text = "This is a test." * 50  # Create a string that exceeds 1000 characters
        parts = list(split_text(text, max_length=1000))
        self.assertTrue(all(len(part) <= 1000 for part in parts))  # All parts have a length not exceeding 1000

    @patch('chatgpymodel.requests.post')
    def test_query_openai(self, mock_post):
        # Mock OpenAI API response
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Mock reply'}}]
        }

        response = query_openai("Test")
        self.assertEqual(response, 'Mock reply')

    def test_get_first_text(self):
        # Test get_first_text function
        self.assertEqual(get_first_text(['Test text']), 'Test text')
        self.assertEqual(get_first_text([]), '')

if __name__ == '__main__':
    unittest.main()
