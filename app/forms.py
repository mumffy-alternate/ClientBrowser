from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    password =  PasswordField('password')

class ProfileForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])