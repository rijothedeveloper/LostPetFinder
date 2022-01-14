from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, InputRequired

class reportPetForm(FlaskForm):
    """ form for report seen pet """
    types = ["Cat",
             "Cow",
             "Dog",
             "Mouse", 
             "Sheep",
             "other"]
    pet_type = SelectField("Pet Type", choices=types, validators=[InputRequired()])
    breed = StringField('Breed', validators=[DataRequired()])
    address = StringField('Location', validators=[DataRequired()])
    comments = TextAreaField("Comments")
    latitude = HiddenField("latitude")
    longitude = HiddenField("longitude")
    
    