import unittest
import uuid
from app.service.database import get_one_url, delete_item
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestShortenUrlIntegrationAPI(unittest.TestCase):
    def test_no_custom_url(self):
        response_post = client.post(url="/api/shorten_url", json={"original_url": "https://www.google.com"})
        self.assertEqual(200, response_post.json()["status_code"])

        short_url = response_post.json()["short_url"]
        db_response = get_one_url(short_url=short_url)
        self.assertEqual(200, db_response["status_code"])

        # Delete item just added to DB
        delete_item(short_url=short_url)

    def test_custom_url_no_collision(self):
        mock_custom_string = str(uuid.uuid4())
        response_post = client.post(url="/api/shorten_url", json={"custom_url": mock_custom_string, "original_url": "https://www.google.com"})
        self.assertEqual(200, response_post.json()["status_code"])

        short_url = response_post.json()["short_url"]
        db_response = get_one_url(short_url=short_url)
        self.assertEqual(200, db_response["status_code"])

        # Delete item just added to DB
        delete_item(short_url=short_url)

    def test_custom_url_with_collision(self):
        custom_url = "existing_url"
        response_check = get_one_url(short_url=custom_url)
        self.assertEqual(200, response_check["status_code"])

        response = client.post(url="/api/shorten_url", json={"custom_url": custom_url, "original_url": "https://www.google.com"})
        self.assertEqual(409, response.json()["status_code"])


if __name__ == '__main__':
    unittest.main()
