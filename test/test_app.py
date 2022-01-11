from unittest import TestCase
from app import app
class test_app(TestCase):
    def test_home_page(self):
         with app.test_client() as client:
            res = client.get("/")
            self.assertEqual(res.status_code, 200)
            