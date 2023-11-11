import unittest
from app.service.database import reset_db


class TestResetDB(unittest.TestCase):
    def test_database_reachable(self):
        # Resets DB after testing to only contain 1 entry --> "existing_url" : "https://www.google.com"
        response = reset_db()
        self.assertEqual(200, response["status_code"])


if __name__ == '__main__':
    unittest.main()
