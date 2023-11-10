import unittest
from app.service.database import reset_db


class TestResetDB(unittest.TestCase):
    def test_database_reachable(self):
        response = reset_db()
        self.assertEqual(200, response["status_code"])


if __name__ == '__main__':
    unittest.main()
