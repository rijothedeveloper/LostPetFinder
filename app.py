from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from forms.forms import SignupForm
from models.models import db, connect_db
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lost_pet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
# db.create_all()

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/")
def show_home():
    return render_template("index.html")

@app.route("/signup")
def addUser():
    """
    Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that email: flash message
    and re-present form.
    """
    
    form = SignupForm()
    return render_template("users/signup-form.html", form=form)