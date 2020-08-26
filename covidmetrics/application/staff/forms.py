"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class StaffUpdateForm(FlaskForm):
    """User Sign-up Form."""

    staff_role_id = SelectField(u'Role', coerce=int, validators=[DataRequired()])

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

    submit = SubmitField('Add Staff Update')

