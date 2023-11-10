import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestListUrlsIntegrationAPI(unittest.TestCase):
    def test_list_urls(self):
        response_raw = client.get(url="/api/list_urls")
        response = response_raw.json()
        self.assertEqual(200, response["status_code"])

        url_list = response["payload"]
        self.assertIsInstance(url_list, list)

        self.assertGreater(len(url_list), 0)


if __name__ == '__main__':
    unittest.main()
