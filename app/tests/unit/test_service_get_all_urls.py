import unittest
from app.service.database import get_all_urls


class TestGetAllUrls(unittest.TestCase):

    def test_successful_retrieval(self):
        response = get_all_urls()
        self.assertEqual(200, response["status_code"])


if __name__ == '__main__':
    unittest.main()
