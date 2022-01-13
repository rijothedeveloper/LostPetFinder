from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, InputRequired

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
    
    