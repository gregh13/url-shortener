import unittest
from app.service.database import get_one_url


class TestGetOneUrl(unittest.TestCase):
    def test_database_reachable(self):
        response = get_one_url("test")
        self.assertNotEqual(response["status_code"], 500)

    def test_url_does_not_exist(self):
        response = get_one_url("nonexistant")
        self.assertEqual(response["status_code"], 404)

    def test_url_exists(self):
        response = get_one_url("existing_url")
        self.assertEqual(response["status_code"], 200)

        # self.assertEqual(response["payload"], "https://www.exisiting_url.com")

    def test_bad_url_inputs(self):
        bad_inputs_1 = [{}, {"url": "test"}, ["testurl"], ("url", "test"), None]
        bad_inputs_2 = [set(), {1}, {"url"}]
        bad_inputs_3 = [True, False, ")(#$*(&&&*", 3.1415]
        all_bad_inputs = [(500, bad_inputs_1), (400, bad_inputs_2), (404, bad_inputs_3)]

        for error_code, bad_input_list in all_bad_inputs:
            for bad_input in bad_input_list:
                response = get_one_url(bad_input)
                self.assertEqual(error_code,
                                 response["status_code"],
                                 msg=f"{bad_input} --> {response["status_code"]}, {response["payload"]}")


if __name__ == '__main__':
    unittest.main()
