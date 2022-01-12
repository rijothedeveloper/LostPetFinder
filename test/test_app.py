from unittest import TestCase
from app import app
class test_app(TestCase):
    
    def test_home_page(self):
         with app.test_client() as client:
            res = client.get("/")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            shouldContain = 'Login'
            self.assertIn(shouldContain, html)
            shouldContain = 'welcome to lost petfinder'
            self.assertIn(shouldContain, html)
            
    def test_signup_page_get(self):
         with app.test_client() as client:
            res = client.get("/signup")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            shouldContain = '<label for="email">E-mail</label>'
            self.assertIn(shouldContain, html)