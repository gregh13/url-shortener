import unittest
import uuid
from app.service.database import delete_item
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestShortenUrlAPI(unittest.TestCase):
    def test_no_custom_url(self):
        response = client.post(url="/api/shorten_url", json={"original_url": "https://www.existing.com"})
        response_code = int(response[:3])
        self.assertEqual(200, response_code)

    def test_custom_url_no_collision(self):
        mock_custom_string = str(uuid.uuid4())
        response = client.post(url="/api/shorten_url", json={"custom_url": mock_custom_string, "original_url": "https://www.existing.com"})
        response_code = int(response[:3])
        self.assertEqual(200, response_code)

        # Delete item just added to DB
        delete_item(mock_custom_string)

    def test_custom_url_with_collision(self):
        custom_url = "existing_url"
        response = client.post(url="/api/shorten_url", json={"custom_url": custom_url, "original_url": "https://www.existing.com"})
        response_code = int(response[:3])
        self.assertEqual(409, response_code)

        # Delete item just added to DB
        delete_item(custom_url)


if __name__ == '__main__':
    unittest.main()