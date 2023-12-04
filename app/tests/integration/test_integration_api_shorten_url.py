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

        # Get short_url that was just added to DB
        short_url = response_post.json()["short_url"]

        # Check that short_url in now in the DB
        db_response = get_one_url(short_url=short_url)
        self.assertEqual(200, db_response["status_code"])

        # Delete item just added to DB
        delete_item(short_url=short_url)

    def test_custom_url_no_collision(self):
        # To ensure no collision, we get a full random string to simulate a custom input
        mock_custom_string = str(uuid.uuid4())
        params = {"custom_url": mock_custom_string, "original_url": "https://www.google.com"}
        response_post = client.post(url="/api/shorten_url", json=params)
        self.assertEqual(200, response_post.json()["status_code"])

        # Get short_url that was just added to DB
        short_url = response_post.json()["short_url"]

        # Check that short_url in now in the DB
        db_response = get_one_url(short_url=short_url)
        self.assertEqual(200, db_response["status_code"])

        # Delete item just added to DB
        delete_item(short_url=short_url)

    def test_custom_url_with_collision(self):
        custom_url = "existing_url"

        # Ensure existing_url is in DB
        response_prepost = get_one_url(short_url=custom_url)
        self.assertEqual(200, response_prepost["status_code"])

        # Ensure original_url is default value
        original_url_initial = response_prepost["payload"].original_url
        default_original = "https://www.google.com"
        self.assertEqual(default_original, original_url_initial)

        # Attempt to overwrite existing_url in DB
        new_original_url = "overwritten.com"
        params = {"custom_url": custom_url, "original_url": new_original_url}
        response_post = client.post(url="/api/shorten_url", json=params)

        # Ensure post request was unsuccessful and PutError occurred
        self.assertEqual(409, response_post.json()["status_code"])

        # Get existing url again, ensure original_url has not been changed
        response_prepost = get_one_url(short_url=custom_url)
        self.assertEqual(200, response_prepost["status_code"])

        # Ensure original_url is still default value and not overwritten
        original_url_final = response_prepost["payload"].original_url
        self.assertEqual(default_original, original_url_final)
        self.assertNotEqual(new_original_url, original_url_final)


if __name__ == '__main__':
    unittest.main()
