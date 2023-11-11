import unittest
import uuid
from app.service.database import add_custom_url_to_db, delete_item


class TestAddCustomUrl(unittest.TestCase):
    def test_url_no_collision(self):
        # To ensure no collision, we get a full random string to simulate a custom input
        mock_custom_string = str(uuid.uuid4())

        add_response = add_custom_url_to_db(custom_url=mock_custom_string, original_url="testing_database")
        self.assertEqual(200, add_response["status_code"])

        # Delete item just added to DB
        delete_item(mock_custom_string)

    def test_url_collision(self):
        response = add_custom_url_to_db(custom_url="existing_url", original_url="https://www.google.com")
        self.assertEqual(409, response["status_code"])

    def test_bad_url_inputs(self):
        # Initialize bad inputs
        bad_inputs_1 = [{}, {"url": "test"}, ["testurl"], ("url", "test")]
        bad_inputs_2 = [set(), {1}, {"url"}, None]

        # Pair input lists with error codes
        all_bad_inputs = [(409, bad_inputs_1), (400, bad_inputs_2)]

        for error_code, bad_input_list in all_bad_inputs:
            for bad_input in bad_input_list:

                response = add_custom_url_to_db(custom_url=bad_input, original_url="test.com")
                message = f"{bad_input} --> {response["status_code"]}, {response["payload"]}"

                if response["status_code"] == 200:
                    # Delete item in case bad_input was somehow added to db
                    delete_item(bad_input)

                self.assertEqual(error_code, response["status_code"], msg=message)


if __name__ == '__main__':
    unittest.main()
