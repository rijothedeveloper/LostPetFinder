from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    """ form for adding users """
    
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=9)])
    address = StringField("Address", validators=[DataRequired(), Length(min=12)])
    latitude = HiddenField("latitude")
    longitude = HiddenField("longitude")
    
    