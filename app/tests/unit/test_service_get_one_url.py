import unittest
from app.service.database import get_one_url


class TestGetOneUrl(unittest.TestCase):
    def test_database_reachable(self):
        response = get_one_url("test")
        self.assertNotEqual(500, response["status_code"])

    def test_url_does_not_exist(self):
        response = get_one_url("nonexistant")
        self.assertEqual(404, response["status_code"])

    def test_url_exists(self):
        response = get_one_url("existing_url")
        self.assertEqual(200, response["status_code"])


    def test_bad_url_inputs(self):
        # Initialize bad inputs
        bad_inputs_1 = [{}, {"url": "test"}, ["testurl"], ("url", "test"), None]
        bad_inputs_2 = [set(), {1}, {"url"}]
        bad_inputs_3 = [True, False, ")(#$*(&&&*", 3.1415]

        # Pair input lists with error codes
        all_bad_inputs = [(500, bad_inputs_1), (400, bad_inputs_2), (404, bad_inputs_3)]

        for error_code, bad_input_list in all_bad_inputs:
            for bad_input in bad_input_list:
                response = get_one_url(bad_input)
                message = f"{bad_input} --> {response["status_code"]}, {response["payload"]}"
                self.assertEqual(error_code, response["status_code"], msg=message)


if __name__ == '__main__':
    unittest.main()
