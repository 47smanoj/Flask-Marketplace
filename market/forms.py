from django.forms import ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, email, DataRequired, ValidationError
from market.model import user

class RegisterForms(FlaskForm):

    def validate_username(self, username_to_validate):
        user1 = user.query.filter_by(username=username_to_validate.data).first()
        if user1:
            raise ValidationError('Username already exist! Please try a different username')

    def validate_email(self, email_to_validate):
        email1 = user.query.filter_by(email=email_to_validate.data).first()
        if email1:
            raise ValidationError('Email Address already exist! Please try a different Email Address')

    username = StringField(label='User Name: ', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email Address: ', validators=[email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name: ', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password: ', validators=[Length(min=8), DataRequired()])
    submit = SubmitField(label='Sign In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')