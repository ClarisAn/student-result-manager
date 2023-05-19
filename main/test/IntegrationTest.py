import unittest
from app import app
import logging

logging.basicConfig(level=logging.INFO)


class IntTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_thing(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
