from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class SignUpForm(FlaskForm):
    email=StringField('Email')
    name=StringField('Full Name')
    password=StringField('Password')
    creditCardNumber=StringField('Card number')
    creditCardExpiration=StringField('Expiration mm/yy')
    cardCVV=StringField('cvv')
    submit=SubmitField('Complete')
