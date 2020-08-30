"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class BusGroupForm(FlaskForm):

    bus_group_id = HiddenField()
    description = StringField()
    district_id = HiddenField()
    available = IntegerField()
    required = IntegerField()

    add = SubmitField('Add')
    update = SubmitField('Save')
    delete = SubmitField('Del')

