import unittest
import uuid
from app.service.database import add_url_to_db, delete_item


class TestAddUrl(unittest.TestCase):
    def test_database_reachable(self):
        random_string = str(uuid.uuid4())
        add_response = add_url_to_db(short_url=random_string, original_url="testing_database")
        self.assertNotEqual(500, add_response["status_code"])

        # Delete item just added to DB
        del_response = delete_item(random_string)
        self.assertEqual(200, del_response["status_code"])


if __name__ == '__main__':
    unittest.main()
