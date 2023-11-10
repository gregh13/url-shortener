import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestListUrlAPI(unittest.TestCase):
    def test_list_urls(self):
        response = client.get(url="/api/list_urls")
        self.assertEqual(200, response.json()["status_code"])


if __name__ == '__main__':
    unittest.main()
