from unittest import TestCase
from app import app
from models.models import db, User, Location, Animal, Lost_animal

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lost_pet_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False

# connect_db(app)
db.drop_all()
db.create_all()

class test_app(TestCase):
   user = ""
   @classmethod
   def setUpClass(cls):
      location = Location(formatted_address="570 w tramonto", latitude=1, longitude=1)
      db.session.add(location)
      db.session.commit()
        
      email = "logicDemo@gmail.com"
      password = "poopoo"
      user = User.signup(email=email, 
                           password=password, 
                           first_name="rijo", 
                           last_name="George", 
                           location_id=location.id, 
                           phone="567890123")
      
      user2 = User.signup(email="logicDemo@gmail.com", 
                           password=password, 
                           first_name="rego", 
                           last_name="George", 
                           location_id=location.id, 
                           phone="567890123")
      
      animal = Animal(type="dog",
                      breed="poodle")
      
      db.session.add(user)
      db.session.add(user2)
      db.session.add(animal)
      db.session.commit()
      lost_pet = Lost_animal(animal_id=animal.id,
                             user_id=user.id,
                             location_id=location.id,
                             image="",
                             comments="no comments")
      
      lost_pet2 = Lost_animal(animal_id=animal.id,
                             user_id=user2.id,
                             location_id=location.id,
                             image="",
                             comments="no comments")
      
      db.session.add(lost_pet)
      db.session.add(lost_pet2)
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
         shouldContain = 'For lost pets'
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
         shouldContain = 'rijo'
         self.assertIn(shouldContain, html)
         
   def test_report_pet(self):
      with app.test_client() as client:
         client.get("/logout")
         resp = client.get("/pet/add",
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
         
         resp = client.get("/pet/add",
                           follow_redirects=True)
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = 'Location'
         self.assertIn(shouldContain, html)
         
         data = { 
                  'pet_type': "Dog",  
                  'breed': "poodle",
                  'comments': "my test comment of new",
                  'address': "570 w tramonto dr",
                  'latitude':1,
                  'longitude':1}
         resp = client.post("/pet/add",
                           data=data,
                           follow_redirects=True)
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = 'my test comment of new'
         self.assertIn(shouldContain, html)
         
   def test_show_lost_pets(self):
      with app.test_client() as client:
         resp = client.get("/browse-pets")
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = '<p>no comments</p>'
         self.assertIn(shouldContain, html)
         
   def test_profile_page(self):
      with app.test_client() as client:
         #  login
         data = { 
                  'email': "logicDemo@gmail.com",  
                  'password': "poopoo" }
         client.post("/login",
                               data= data,
                               follow_redirects=True)
         
         resp = client.get("/users/1")
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = 'rijo'
         self.assertIn(shouldContain, html)
         # check edit button is there or not
         shouldContain = '<button class="btn btn-border">Save</button>'
         self.assertIn(shouldContain, html)
         # check user reported pets are showing
         shouldContain = 'details'
         self.assertIn(shouldContain, html)
         
         # test edit profile submission
         data = { 
                  'email': "testuser@test.com",  
                  'password': "mypass",
                  'first_name': "rego",
                  'last_name': "George",
                  'phone': "123456789",
                  'address': "570 w tramonto dr",
                  }
         resp = client.post("/users/1", data=data)
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = 'rego'
         self.assertIn(shouldContain, html)
         
         
   def test_edit_pet(self):
      with app.test_client() as client:
         # make sure return 404 for invalid pet id
         resp = client.get("/pet/125/edit")
         self.assertEqual(resp.status_code, 404)
         
         # make sure user can delete his on reportings
         resp = client.get("/pet/2/edit")
         self.assertEqual(resp.status_code, 302)
         
         # make sure edit form is shown for users pet
         #  login
         data = { 
                  'email': "logicDemo@gmail.com",  
                  'password': "poopoo" }
         client.post("/login",
                               data= data,
                               follow_redirects=True)
         resp = client.get("/pet/1/edit")
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = 'no comments'
         self.assertIn(shouldContain, html)
         
   def test_edit_pet_post(self):
      with app.test_client() as client:
         #  login
         data = { 
                  'email': "logicDemo@gmail.com",  
                  'password': "poopoo" }
         client.post("/login",
                               data= data,
                               follow_redirects=True)
         
         data = { 
                  'pet_type': "Dog",  
                  'breed': "poodle poodle",
                  'comments': "my test comment",
                  'address': "570 w tramonto dr",
                  'latitude':1,
                  'longitude':1}
         resp = client.post("/pet/1/edit",
                           data=data,
                           follow_redirects=True)
         self.assertEqual(resp.status_code, 200)
         html = resp.get_data(as_text=True)
         shouldContain = 'poodle poodle'
         self.assertIn(shouldContain, html)