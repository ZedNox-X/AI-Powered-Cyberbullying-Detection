import os
import tempfile
import unittest

os.environ["SECRET_KEY"] = "test-secret"
from app import app

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_health(self):
        self.assertEqual(self.client.get("/health").status_code, 200)

if __name__ == "__main__":
    unittest.main()
