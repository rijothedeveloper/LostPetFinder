from flask import Flask, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from forms.forms import SignupForm
from models.models import db, connect_db, Location, User
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
CURR_USER_KEY = "curr_user"

# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lost_pet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
# db.create_all()

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None
        
        
def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/")
def show_home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def addUser():
    """
    Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that email: flash message
    and re-present form.
    """
    
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        formatted_address = form.address.data
        latitude = form.latitude.data
        longitude = form.longitude.data
        location = Location(formatted_address=formatted_address, latitude=latitude, longitude=longitude)
        db.session.add(location)
        db.session.commit()
        id=location.id
        new_user = User.signup(email=email,password=password, first_name=first_name, last_name=last_name, location_id=location.id, phone=phone)
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            do_login(new_user)
            flash(f"{new_user.email} added", 'cat-success')
            return redirect("/")
        else:
             flash("error in form submission", 'cat-error')
        
    return render_template("users/signup-form.html", form=form)



##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req