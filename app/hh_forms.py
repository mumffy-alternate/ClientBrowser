from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, HiddenField, SelectField, DateTimeField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email
from wtforms_components import TimeField

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


class CaseForm(FlaskForm):
    date_opened = StringField('date_opened')
    date_closed = StringField('date_closed')
    case_name = StringField('case_name', validators=[Length(2, 255), DataRequired()])
    court_case_number = StringField('court_case_number', validators=[Length(max=255)])

    def __init__(self, case=None, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        if case is not None:
            self.case_name.data = case.case_name
            self.date_opened.data = case.date_opened.strftime('%Y-%m-%d') if case.date_opened else None
            self.date_closed.data = case.date_closed.strftime('%Y-%m-%d') if case.date_closed else None
            self.court_case_number.data = case.court_case_number

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        if str(self.case_name).find('/') == -1:
            self.case_name.errors.append("Case Name must contain a slash, for example \"Eggplant/Grapefruit\"")
            return False

        return True

class PhoneLogForm(FlaskForm):
    logdate = StringField('logdate', validators=[DataRequired()])
    logtime = StringField('logtime', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])