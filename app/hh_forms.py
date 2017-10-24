from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, DateField, HiddenField, SelectField
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
    birthdate = DateField('birthdate')
    sex = StringField('sex', validators=[Length(max=15)])
    # case_id = StringField
    role_id = SelectField('rold_id')
    role_comment = StringField('role_comment', validators=[Length(max=127)])

