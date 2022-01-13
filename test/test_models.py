from unittest import TestCase
from app import app
from models.models import db, connect_db, User, Location

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lost_pet_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# connect_db(app)
db.drop_all()
db.create_all()

class test_user(TestCase):
    email = ""
    password = ""
    def setUp(self):
        location = Location(formatted_address="570 w tramonto", latitude=1, longitude=1)
        db.session.add(location)
        db.session.commit()
        
        self.email = "logicDemo@gmail.com"
        self.password = "poopoo"
        user = User.signup(email=self.email, password=self.password, first_name="rego", last_name="George", location_id=1, phone="567890123")
        db.session.add(user)
        db.session.commit()
        
    def tearDown(self):
        db.session.rollback()
        User.query.delete()
        db.session.commit()
        
    def test_signup(self):
        email = "logic@gmail.com"
        password = "poopoo"
        user = User.signup(email=email, password=password, first_name="rego", last_name="George", location_id=1, phone="567890123")
        self.assertEqual(email, user.email)
        self.assertNotEqual(password, user.password)
        
    def test_authentication(self):
        user = User.autenticate(email="logi@gmail.com", password="hello")
        self.assertEqual(user, False)
        
        user = User.autenticate(email="logi@gmail.com", password=self.password)
        self.assertEqual(user, False)
        
        user = User.autenticate(email=self.email, password="hello")
        self.assertEqual(user, False)
        
        user = User.autenticate(email=self.email, password=self.password)
        self.assertEqual(user.email, self.email)
    