from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, InputRequired

class AlertForm(FlaskForm):
    """ form for create an alert """
    types = ["Cat",
             "Cow",
             "Dog",
             "Mouse", 
             "Sheep",
             "other"]
    mileChoices = [5, 10,25,50,75,100]
    pet_type = SelectField("Pet Type", choices=types, default="Cat", validators=[InputRequired()])
    breed = StringField("Breed")
    radius = SelectField("Radius", choices=mileChoices, default=5, validators=[InputRequired()])
    