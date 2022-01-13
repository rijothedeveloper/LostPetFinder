from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
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
    
    email = db.Column(db.Text,
                    nullable=False)
    
    password = db.Column(db.Text,
                        nullable=False)
    
    first_name = db.Column(db.Text,
                    nullable=False)
    
    last_name = db.Column(db.Text,
                    nullable=False)
    
    location_id = db.Column(db.Integer,
                           db.ForeignKey('location.id', ondelete="CASCADE"))
    phone = db.Column(db.Text)
    
    
    def __repr__(self):
        return f"<User #{self.id}: {self.first_name}, {self.last_name}, {self.email}>"
    
    @classmethod
    def signup(cls, email, password, first_name, last_name, location_id, phone):
        """Sign up user.
        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        
        user = User(email=email, 
                    password=hashed_pwd, 
                    first_name=first_name, 
                    last_name=last_name, 
                    location_id=location_id, 
                    phone=phone)
        
        db.session.add(user)
        return user
    
    @classmethod
    def autenticate(cls, email, password):
        """
        Find user with `username` and `password`.
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """
        
        user = cls.query.filter_by(username=username).first()
        
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    
    
class Location(db.Model):
    """ location """
    
    __tablename__ = "location"
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    formatted_address = db.Column(db.Text,
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