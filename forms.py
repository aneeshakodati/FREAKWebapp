from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, IntegerField, SelectField


class SignUpForm(FlaskForm):
    email=StringField('Email')
    name=StringField('Full Name')
    password=StringField('Password')
    creditCardNumber=StringField('Card number')
    creditCardExpiration=StringField('Expiration mm/yy')
    cardCVV=StringField('cvv')
    submit=SubmitField('Complete')


class OrderFood(FlaskForm):
    email=StringField('Email')
    item = SelectField(
        'Item',

        choices=[
            ('Burrito', 'burrito'),
            ('Bowl', 'bowl'),
        ]
    )
    quantity=IntegerField(' Quantity')
    type = SelectField(
        'Rice & Tortilla',

        choices=[
            ('Whole wheat tortilla/rice', 'whole wheat'),
            ('Regular', 'regular'),
        ]
    )
    pico = SelectField(
        'Pico de Gallo',

        choices=[
            ('Yes', 'yes'),
            ('No', 'no' ),
        ]
    )
    beans = SelectField(
        'Beans',

        choices=[
            ('Black beans', 'black'),
            ('Red beans', 'red'),
            ('No beans', 'none'),
        ]
    )
    submit=SubmitField('Order now')
