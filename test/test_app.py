from unittest import TestCase
from app import app
from models.models import db, User, Location

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lost_pet_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False

# connect_db(app)
db.drop_all()
db.create_all()

class test_app(TestCase):
   
   @classmethod
   def setUpClass(cls):
      location = Location(formatted_address="570 w tramonto", latitude=1, longitude=1)
      db.session.add(location)
      db.session.commit()
        
      email = "logicDemo@gmail.com"
      password = "poopoo"
      user = User.signup(email=email, 
                           password=password, 
                           first_name="rego", 
                           last_name="George", 
                           location_id=1, 
                           phone="567890123")
        
      db.session.add(user)
      db.session.commit()
        
   @classmethod
   def tearDownClass(cls):
      db.session.rollback()
      User.query.delete()
      Location.query.delete()
      db.session.commit()
    
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
            
   def test_login_get(self):
      with app.test_client() as client:
         res = client.get("/login")
         self.assertEqual(res.status_code, 200)
         html = res.get_data(as_text=True)
         shouldContain = '<label for="email">E-mail</label>'
         self.assertIn(shouldContain, html)
            
   def test_login_post(self):
      with app.test_client() as client:
         data = { 
                  'email': "logicDemo@gmail.com",  
                  'password': "poopoo" }
         resp = client.post("/login",
                               data= data,
                               follow_redirects=True)
         self.assertEqual(resp.status_code, 200)
         
         html = resp.get_data(as_text=True)
         shouldContain = 'rego'
         self.assertIn(shouldContain, html)
         
   def test_report_pet(self):
      with app.test_client() as client:
         client.get("/logout")
         resp = client.get("reportPet",
                           follow_redirects=True)
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = '<label for="email">E-mail</label>'
         self.assertIn(shouldContain, html)
         
         #  login
         data = { 
                  'email': "logicDemo@gmail.com",  
                  'password': "poopoo" }
         client.post("/login",
                               data= data,
                               follow_redirects=True)
         
         resp = client.get("reportPet",
                           follow_redirects=True)
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = 'Location'
         self.assertIn(shouldContain, html)
         
         data = { 
                  'type': "dog",  
                  'breed': "poodle",
                  'comments': "none",
                  'address': "570 w tramonto dr",
                  'latitude':1,
                  'longitude':1}
         resp = client.post("reportPet",
                           data=data,
                           follow_redirects=True)
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = 'rego'
         self.assertIn(shouldContain, html)
      