from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

from app.models import User

class LoginForm(FlaskForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    password =  PasswordField('password')

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        user = User.query.filter_by(nickname=self.user_name.data).first()

        if user is None:
            self.user_name.errors.append("{0} is not a registered user".format(self.user_name.data))
            return False

        if self.password.data != "secret":
            self.password.errors.append("Password incorrect")
            return False

        return True

class ProfileForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_email, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_email = original_email

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        if self.email.data == self.original_email:
            return True

        user = User.query.filter_by(email=self.email.data).first() # TODO concurrency issue?
        if user != None:
            self.email.errors.append("This e-mail address is already in use.  Please provide a different one.")
            return False

        return True

class PostForm(FlaskForm):
    post = StringField('post', validators=[DataRequired()])
