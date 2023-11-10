import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRedirectAPI(unittest.TestCase):
    def test_existing_url_redirect(self):
        valid_url = "existing_url"
        url = f"/api/redirect/{valid_url}"
        response = client.get(url=url)
        self.assertEqual(200, response.status_code)

    def test_non_existing_url_redirect(self):
        invalid_url = "non_existing_url"
        url = f"/api/redirect/{invalid_url}"
        response = client.get(url=url)
        self.assertEqual(404, response.json()["status_code"])

    def test_no_input_redirect(self):
        no_input = ""
        url = f"/api/redirect/{no_input}"
        response = client.get(url=url)
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
