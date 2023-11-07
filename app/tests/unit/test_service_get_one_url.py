import unittest
from app.service.database import get_one_url


class GetOneUrl(unittest.TestCase):
    def test_database_reachable(self):
        response = get_one_url("test")
        self.assertNotEquals(response["status_code"], 500)

    def test_url_does_not_exist(self):
        response = get_one_url("nonexistant")
        self.assertEqual(response["status_code"], 404)

    def test_url_exists(self):
        response = get_one_url("existing_url")
        self.assertEqual(response["status_code"], 200)

        # self.assertEqual(response["payload"], "https://www.exisiting_url.com")

    def test_bad_url_inputs(self):
        all_bad_input = [set(), {}, {1}, {"url": "test"}, "*(#&$)(&@(#", 3.1415, ["testurl"], (1), True, False, None]

        for bad_input in all_bad_input:
            response = get_one_url(bad_input)
            self.assertEqual(response, 400)


if __name__ == '__main__':
    unittest.main()
