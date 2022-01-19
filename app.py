from flask import Flask, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from forms.alert_form import AlertForm
from forms.edit_pet_form import EditPetForm
from forms.forms import SignupForm
from forms.login_form import LoginForm
from forms.report_pet_form import ReportPetForm
from models.models import Animal, db, connect_db, Location, User, Lost_animal, Alert
from werkzeug.utils import secure_filename
from sqlalchemy import or_
import requests
from celery import Celery
from flask_mail import Mail, Message
from secret import getPass


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
CURR_USER_KEY = "curr_user"

# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lost_pet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "clothlog@gmail.com"
app.config['MAIL_PASSWORD'] = getPass()
app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'

# Initialize mail extensions
mail = Mail(app)

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
        
def isLogged():
    if CURR_USER_KEY in session:
        return True
    return False

def get_recent_lost_pets():
    lost_pets = Lost_animal.query.all()
    return lost_pets

def get_pets():
    lost_pets = Lost_animal.query.filter(Lost_animal.user_id == g.user.id).all()
    return lost_pets

@celery.task
def sendEmail(alertEmails, lost_animal):
    for email in alertEmails:
        # send the email
        email_data = {
            'subject': f'new {lost_animal.animal.type} reported',
            'to': email,
            'body': f'A new animal of {lost_animal.animal.type} and breed {lost_animal.animal.breed} is found, please visit http://127.0.0.1:5000/pet/{lost_animal.id}'
        }
        msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
        msg.body = email_data['body']
        with app.app_context():
            mail.send(msg)  
        
def isValidDistance(animal_location, alert_location, within):
    query = {'origins':f"{animal_location.latitude},{animal_location.longitude}", 
             'destinations':f"{alert_location.latitude},{alert_location.longitude}",
             'units' : 'imperial',
             'key' : 'AIzaSyAleLWSoj4wIihOMwdStcPdztvvg5JmxqA'}
    try:
        response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json', params=query)
        response.raise_for_status()
        distanceMatrix = response.json()
        distance_str = distanceMatrix['rows'][0]['elements'][0]['distance']['text']
        distance = float(distance_str.replace(" mi",""))
        if distance <= within:
            return True
        return False
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)
  
def getAlertEmails(lost_animal):
    alerts = db.session.query(Alert).filter(Alert.type == lost_animal.animal.type).filter(or_(Alert.breed == lost_animal.animal.breed, Alert.breed == "")).all()
    alertEmails = []
    for alert in alerts:
        if isValidDistance(lost_animal.location, alert.location, alert.within):
            user = User.query.get(alert.user_id)
            alertEmails.append(user.email)
    return alertEmails

# @celery.task  
def sendAlert(lost_animal):
    alertEmails = getAlertEmails(lost_animal)
    
    # sendEmail.apply_async(args=[email_data])
    sendEmail(alertEmails, lost_animal)

@app.route("/")
def show_home():
    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': "rijogeorge7@gmail.com",
        'body': 'This is a test email sent from a background Celery task.'
    }
    # task = sendEmail.delay(email_data)
    # sendEmail.apply_async(args=[email_data])
    lost_pets = get_recent_lost_pets()
    return render_template("index.html", lost_pets=lost_pets)

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
            flash(f"{new_user.email} added", 'success')
            return redirect("/")
        else:
             flash("error in creating user", 'error')
        
    return render_template("users/signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.autenticate(email=email, password=password)
        if user:
            do_login(user)
            flash(f"{user.full_name} successfully logged in", 'success')
        else:
            flash("not a valid user", 'error')
            
        return redirect("/")
    
    else:
        return render_template("users/login-form.html", form=form)
    
@app.route("/logout")
def logout():
    do_logout()
    flash(f"{g.user.full_name} successfully logged out", 'success')
    return redirect("/")

@app.route("/browse-pets")
def show_pets():
    lost_pets = get_recent_lost_pets()
    return render_template("pets/show-reported-pets.html", lost_pets=lost_pets)

@app.route("/pet/<int:petId>")
def showPetDetails(petId):
    pet = Lost_animal.query.get_or_404(petId)
    return render_template("pets/show-reported-pet.html", lost_pet=pet)

#############################################################################
#Logged in area

#############################################################################

@app.route("/users/<int:user_id>", methods=["GET", "POST"])
def show_profile(user_id):
    if not isLogged():
        flash("please login", "error")
        return redirect("/login")
    
    # check the url for currently logged in user
    if user_id != g.user.id:
        flash("wrong user, login first", "error")
        return redirect("/login")
    form = SignupForm(obj=g.user)
    if form.validate_on_submit():
        g.user.email = form.email.data
        g.user.password = form.password.data
        g.user.first_name = form.first_name.data
        g.user.last_name = form.last_name.data
        g.user.phone = form.phone.data
        g.user.formatted_address = form.address.data
        if form.latitude.data:
            g.user.location.latitude = form.latitude.data
        if form.longitude.data:
            g.user.location.longitude = form.longitude.data
        db.session.commit()
    
    lost_pets = get_pets()
    alerts = Alert.query.all()
    return render_template("users/profile.html", form=form, user=g.user, lost_pets=lost_pets, alerts=alerts)
    

@app.route("/pet/add", methods=["GET", "POST"])
def reportPet():
    if not isLogged():
        return redirect("/login")
    form = ReportPetForm()
    if form.validate_on_submit():
        type = form.pet_type.data
        breed = form.breed.data
        comments = form.comments.data
        formatted_address = form.address.data
        if(form.image.data != '' and form.image.data != None):
            imageName = secure_filename(form.image.data.filename)
            if(len(imageName) > 0):
                form.image.data.save('static/uploaded_pet_images/' + imageName)
        else:
            imageName = ""
        latitude = form.latitude.data
        longitude = form.longitude.data
        location = Location(formatted_address=formatted_address, latitude=latitude, longitude=longitude)
        db.session.add(location)
        animal = Animal(type=type, breed=breed)
        db.session.add(animal)
        db.session.commit()
        lost_animal = Lost_animal(animal_id=animal.id, user_id=g.user.id, location_id=location.id, image=imageName, comments=comments)
        try:
            db.session.add(lost_animal)
            db.session.commit()
            sendAlert(lost_animal)
            flash(f"{animal.type} is reported as found at {location.formatted_address}")
            return redirect("/")
        except Exception as e:
            flash(f"Pet is not reported {e}")
    return render_template("pets/report-pet-form.html", form=form)

@app.route("/pet/<int:petId>/edit", methods=["GET", "POST"])
def editPet(petId):
    lost_pet = Lost_animal.query.get_or_404(petId)
    if g.user == None or lost_pet.user_id != g.user.id:
        flash("not autherised to edit this pet", "error")
        return redirect("/login")
    form = EditPetForm(obj=lost_pet)
    if form.validate_on_submit():
        location = lost_pet.location
        animal = lost_pet.animal
        animal.type = form.pet_type.data
        animal.breed = form.breed.data
        lost_pet.comments = form.comments.data
        location.formatted_address = form.address.data
        if form.latitude.data:
            location.latitude = form.latitude.data
        if form.longitude.data:
            location.longitude = form.longitude.data
        if(form.image.data != '' and form.image.data != None):
            imageName = secure_filename(form.image.data.filename)
            if imageName !="":
                form.image.data.save('static/uploaded_pet_images/' + imageName)
                lost_pet.image = imageName
        
        db.session.commit()
        return redirect(f"/users/{lost_pet.user_id}")
        
    return render_template("/pets/edit-pet-form.html", form=form, lost_pet=lost_pet)

@app.route("/setAlert", methods=["GET", "POST"])
def setAlert():
    if g.user == None :
        flash("not autherised to edit this pet", "error")
        return redirect("/login")
    form = AlertForm()
    if form.validate_on_submit():
        pet_type = form.pet_type.data
        breed = form.breed.data
        radius = form.radius.data
        alert= Alert(user_id=g.user.id, location_id=g.user.location_id, type=pet_type, breed=breed, within=radius)
        db.session.add(alert)
        db.session.commit()
        flash("alert created successfully", "success")
        return redirect(f"/users/{g.user.id}")
    return render_template("/users/create-alert-form.html", form=form)

        


@app.route("/pet/<int:petId>/delete", methods=["GET", "POST"])
def delete_pet(petId):
    lost_pet = Lost_animal.query.get_or_404(petId)
    if g.user == None or lost_pet.user_id != g.user.id:
        flash("not autherised to delete this pet", "error")
        return redirect("/login")
    Lost_animal.query.filter(Lost_animal.id == petId).delete()
    db.session.commit()
    return redirect(f"/users/{lost_pet.user_id}")
    

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