import unittest
from unittest import mock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def mocked_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, response_data):
            self.response_data = response_data

        def json(self):
            return self.response_data

    response = {
        "short_url": None,
        "status_code": None,
        "payload": ''
    }

    if args[0] == "/api/list_urls" or args[0].find("/api/list/urls?") == 0:
        response["status_code"] = 200
        response["payload"] = [{"short_url": "existing_url", "original_url": "https://www.google.com"}]
    else:
        response["status_code"] = 400
        response["payload"] = []

    return MockResponse(response)


class TestListUrlAPI(unittest.TestCase):
    @mock.patch('app.route', side_effect=mocked_response)
    def test_list_urls2(self):
        response = client.get(url="/api/list_urls")
        self.assertEqual(200, response.json()["status_code"])


if __name__ == '__main__':
    unittest.main()
