from unittest import TestCase
from app import app
from models.models import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lost_pet_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# connect_db(app)
db.drop_all()
db.create_all()

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
            
    def test_signup_page_post(self):
        with app.test_client() as client:
            data = { 
                        'email': "testuser@test.com",  
                        'password': "mypass",
                        'first_name': "rijo",
                        'last_name': "George",
                        'phone': "123456789",
                        'address': "570 w tramonto dr",
                        'latitude':1,
                        'longitude':1}
            
            resp = client.post("/signup",
                               data= data,
                               follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            
            html = resp.get_data(as_text=True)
            shouldContain = 'rijo'
            self.assertIn(shouldContain, html)