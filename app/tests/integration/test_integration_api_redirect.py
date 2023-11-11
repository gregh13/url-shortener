import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRedirectAPI(unittest.TestCase):
    def test_existing_url_redirect(self):
        valid_url = "existing_url"
        url = f"/api/redirect/{valid_url}"
        response = client.get(url=url)
        history = response.history
        self.assertEqual("https://www.google.com", response.url)
        self.assertEqual(200, response.status_code)
        self.assertGreater(len(history), 0)
        self.assertTrue(response.history[0].is_redirect)

    def test_non_existing_url_redirect(self):
        invalid_url = "non_existing_url"
        url = f"/api/redirect/{invalid_url}"
        response = client.get(url=url)
        # get response gives 200 even with invalid url, need to access database response dictionary
        response_status_code = response.json()["status_code"]
        history = response.history
        self.assertEqual("http://testserver/api/redirect/non_existing_url", response.url)
        self.assertEqual(404, response_status_code)
        self.assertEqual(0, len(history))

    def test_no_input_redirect(self):
        no_input = ""
        url = f"/api/redirect/{no_input}"
        response = client.get(url=url)
        history = response.history
        self.assertEqual(404, response.status_code)
        self.assertEqual(0, len(history))


if __name__ == '__main__':
    unittest.main()
