"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, SelectField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class StaffUpdateForm(FlaskForm):
    """User Sign-up Form."""

    role_type_id = SelectField(u'Role', coerce=int, validators=[DataRequired()])

    facility_id = SelectField(u'Facility', validators=[DataRequired()])

    required = IntegerField(
        'Required',
        validators=[
            DataRequired()
        ]
    )
    available = IntegerField(
        'Available',
        validators=[
            DataRequired()
        ]
    )

    add = SubmitField('Add')
    update = SubmitField('Save')
    delete = SubmitField('Del')

class StaffUpdateChangeForm(StaffUpdateForm):

    update_id = HiddenField()
    role_type_id = HiddenField()
    facility_id = HiddenField()

