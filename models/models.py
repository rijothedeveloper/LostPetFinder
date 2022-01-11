from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """ connect to a database """
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """ user """
    
    __tablename__ = "user"
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    first_name = db.Column(db.Text,
                    nullable=False)
    
    last_name = db.Column(db.Text,
                    nullable=False)
    
    location_id = db.Column(db.Integer,
                           db.ForeignKey('location.id', ondelete="CASCADE"))
    phone = db.Column(db.Text)
    
    email = db.Column(db.Text,
                    nullable=False)
    
    
    
class Location(db.Model):
    """ location """
    
    __tablename__ = "location"
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    street = db.Column(db.Text,
                    nullable=False)
    
    city = db.Column(db.Text,
                    nullable=False)
    
    state = db.Column(db.Text,
                    nullable=False)
    
    zip = db.Column(db.Text,
                    nullable=False)
    
    country = db.Column(db.Text,
                    nullable=False)
    
    latitude = db.Column(db.Float,
                    nullable=False)
    
    longitude = db.Column(db.Float,
                    nullable=False)
    
class Animal(db.Model):
    """ animal """
    
    __tablename__ = "animal"
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    type = db.Column(db.Text,
                    nullable=False)
    
    breed = db.Column(db.Text)
    
class lost_animal(db.Model):
    """ lost_animal """
    
    __tablename__ = "lost_animal"
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    animal_id = db.Column(db.Integer, 
                          db.ForeignKey('animal.id', ondelete="CASCADE"))
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id', ondelete="CASCADE"))
    
    location_id = db.Column(db.Integer,
                           db.ForeignKey('location.id', ondelete="CASCADE"))
    
    comments = db.Column(db.Text)
    
class alert(db.Model):
    """ alert """
    
    __tablename__ = "alert"
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id', ondelete="CASCADE"))
    
    animal_id = db.Column(db.Integer, 
                          db.ForeignKey('animal.id', ondelete="CASCADE"))
    
    location_id = db.Column(db.Integer,
                           db.ForeignKey('location.id', ondelete="CASCADE"))
    
    within = db.Column(db.Integer)