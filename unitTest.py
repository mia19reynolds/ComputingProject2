import unittest
import requests

class TestAPIConnection(unittest.TestCase):
    """Test case for API connection"""

    def test_api_connection(self):
        """Test if the application can connect to the API"""
        
        api_url = 'https://api.spoonacular.com/recipes/complexSearch' 
        try:
            response = requests.get(api_url)
            # Check if the status code is successful (e.g., 200)
            self.assertEqual(response.status_code, 200)
        except requests.ConnectionError:
            # If the connection fails, fail the test
            self.fail(f"Failed to connect to the API at {api_url}")

if __name__ == '__main__':
    unittest.main()
