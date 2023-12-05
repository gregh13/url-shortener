import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestListUrlsIntegrationAPI(unittest.TestCase):
    def test_list_urls_normal(self):
        response_raw = client.get(url="/api/list_urls")
        response = response_raw.json()
        self.assertEqual(200, response["status_code"])

        # Make sure response has returned a list of urls
        url_list = response["payload"]
        self.assertIsInstance(url_list, list)

        # Make sure list has at least one entry ("existing_url" will always be in the DB for testing)
        self.assertGreater(len(url_list), 0)

    def test_list_urls_bad_input1(self):
        response_raw = client.get(url="/api/list_urls?someparam")
        response = response_raw.json()
        self.assertEqual(200, response["status_code"])

        # Make sure response has returned a list of urls
        url_list = response["payload"]
        self.assertIsInstance(url_list, list)

        # Make sure list has at least one entry ("existing_url" will always be in the DB for testing)
        self.assertGreater(len(url_list), 0)

    def test_list_urls_bad_input2(self):
        response_raw = client.get(url="/api/list_urls?param=data")
        response = response_raw.json()
        self.assertEqual(200, response["status_code"])

        # Make sure response has returned a list of urls
        url_list = response["payload"]
        self.assertIsInstance(url_list, list)

        # Make sure list has at least one entry ("existing_url" will always be in the DB for testing)
        self.assertGreater(len(url_list), 0)

if __name__ == '__main__':
    unittest.main()
