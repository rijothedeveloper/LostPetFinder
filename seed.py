from app import app
from models.models import db, connect_db
connect_db(app)
db.drop_all()
db.create_all()