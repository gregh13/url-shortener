import unittest
import uuid
from app.service.database import add_random_url_to_db, delete_item


class TestAddRandomUrl(unittest.TestCase):
    def test_random_url(self):
        response = add_random_url_to_db(original_url="https://www.exisiting_url.com")
        self.assertEqual(200, response["status_code"])


if __name__ == '__main__':
    unittest.main()
