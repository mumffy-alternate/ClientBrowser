from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, HiddenField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email

from app.models import User

class ClientForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired(), Length(1, 255)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(1, 255)])
    address_line1 = StringField('address_line1', validators=[Length(max=255)])
    address_line2 = StringField('address_line2', validators=[Length(max=255)])
    address_city = StringField('address_city', validators=[Length(max=255)])
    address_state = StringField('address_state', validators=[Length(max=2)])
    address_postal_code = StringField('address_postal_code', validators=[Length(max=30)])
    address_country = StringField('address_country', validators=[Length(max=3)])
    birthdate = StringField('birthdate')
    sex = StringField('sex', validators=[Length(max=15)])
    # case_id = StringField
    # role_id = SelectField('rold_id')
    role_comment = StringField('role_comment', validators=[Length(max=127)])

