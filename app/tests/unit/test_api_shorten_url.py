import unittest
import uuid
from app.service.database import delete_item
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestShortenUrlAPI(unittest.TestCase):
    def test_no_custom_url(self):
        response = client.post(url="/api/shorten_url", json={"original_url": "https://www.google.com"})
        self.assertEqual(200, response.json()["status_code"])

    def test_custom_url_no_collision(self):
        # To ensure no collision, we get a full random string to simulate a custom input
        mock_custom_string = str(uuid.uuid4())

        params = {"custom_url": mock_custom_string, "original_url": "https://www.existing.com"}
        response = client.post(url="/api/shorten_url", json=params)

        self.assertEqual(200, response.json()["status_code"])

        # Delete item just added to DB
        delete_item(mock_custom_string)

    def test_custom_url_with_collision(self):
        custom_url = "existing_url"
        params = {"custom_url": custom_url, "original_url": "https://www.google.com"}
        response = client.post(url="/api/shorten_url", json=params)

        self.assertEqual(409, response.json()["status_code"])


if __name__ == '__main__':
    unittest.main()
