import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRedirectAPI(unittest.TestCase):
    def test_existing_url_redirect1(self):
        valid_url = "existing_url"
        url = f"/api/redirect/{valid_url}"
        response = client.get(url=url)
        self.assertEqual("https://www.google.com", response.url)
        self.assertEqual(200, response.status_code)

        history = response.history

        # Check history has at least one previous page, signalling redirection
        self.assertGreater(len(history), 0)

        # Check redirection status
        self.assertTrue(response.history[0].is_redirect)

    def test_existing_url_redirect2(self):
        valid_url = "existing_url"
        url = f"/api/redirect/{valid_url}?someparams"
        response = client.get(url=url)
        self.assertEqual("https://www.google.com", response.url)
        self.assertEqual(200, response.status_code)

        history = response.history

        # Check history has at least one previous page, signalling redirection
        self.assertGreater(len(history), 0)

        # Check redirection status
        self.assertTrue(response.history[0].is_redirect)

    def test_existing_url_redirect3(self):
        valid_url = "existing_url"
        url = f"/api/redirect/{valid_url}?params=data"
        response = client.get(url=url)
        self.assertEqual("https://www.google.com", response.url)
        self.assertEqual(200, response.status_code)

        history = response.history

        # Check history has at least one previous page, signalling redirection
        self.assertGreater(len(history), 0)

        # Check redirection status
        self.assertTrue(response.history[0].is_redirect)

    def test_non_existing_url_redirect1(self):
        invalid_url = "non_existing_url"
        url = f"/api/redirect/{invalid_url}"
        response = client.get(url=url)

        # Only DB knows this is invalid, so need to access database response status code
        response_status_code = response.json()["status_code"]

        # Client stores request url as current url when redirect fails
        self.assertEqual(f"http://testserver/api/redirect/{invalid_url}", response.url)
        self.assertEqual(404, response_status_code)

        history = response.history

        # Check for empty page history, signalling no redirection occurred
        self.assertEqual(0, len(history))

    def test_non_existing_url_redirect2(self):
        invalid_url = "&(*#$@^@"
        url = f"/api/redirect/{invalid_url}"
        response = client.get(url=url)

        # Only DB knows this is invalid, so need to access database response status code
        response_status_code = response.json()["status_code"]

        # Client stores request url as current url when redirect fails
        self.assertEqual(f"http://testserver/api/redirect/{invalid_url}", response.url)
        self.assertEqual(404, response_status_code)

        history = response.history

        # Check for empty page history, signalling no redirection occurred
        self.assertEqual(0, len(history))

    def test_non_existing_url_redirect3(self):
        invalid_url = "&(*#$@^@?someparams"
        url = f"/api/redirect/{invalid_url}"
        response = client.get(url=url)

        # Only DB knows this is invalid, so need to access database response status code
        response_status_code = response.json()["status_code"]

        # Client stores request url as current url when redirect fails
        self.assertEqual(f"http://testserver/api/redirect/{invalid_url}", response.url)
        self.assertEqual(404, response_status_code)

        history = response.history

        # Check for empty page history, signalling no redirection occurred
        self.assertEqual(0, len(history))

    def test_non_existing_url_redirect4(self):
        invalid_url = "&(*#$@^@?params=data"
        url = f"/api/redirect/{invalid_url}"
        response = client.get(url=url)

        # Only DB knows this is invalid, so need to access database response status code
        response_status_code = response.json()["status_code"]

        # Client stores request url as current url when redirect fails
        self.assertEqual(f"http://testserver/api/redirect/{invalid_url}", response.url)
        self.assertEqual(404, response_status_code)

        history = response.history

        # Check for empty page history, signalling no redirection occurred
        self.assertEqual(0, len(history))

    def test_no_input_redirect1(self):
        no_input = ""
        url = f"/api/redirect/{no_input}"
        response = client.get(url=url)
        self.assertEqual(404, response.status_code)

        history = response.history

        # Check for empty page history, signalling no redirection occurred
        self.assertEqual(0, len(history))

    def test_no_input_redirect2(self):
        no_input = ""
        url = f"/api/redirect/{no_input}?someparams"
        response = client.get(url=url)
        self.assertEqual(404, response.status_code)

        history = response.history

        # Check for empty page history, signalling no redirection occurred
        self.assertEqual(0, len(history))

    def test_no_input_redirect3(self):
        no_input = ""
        url = f"/api/redirect/{no_input}?params=data"
        response = client.get(url=url)
        self.assertEqual(404, response.status_code)

        history = response.history

        # Check for empty page history, signalling no redirection occurred
        self.assertEqual(0, len(history))


if __name__ == '__main__':
    unittest.main()
