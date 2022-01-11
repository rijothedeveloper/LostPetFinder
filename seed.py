from app import app
from models.models import db, connect_db
connect_db(app)
db.create_all()