"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from .models import District

class SignupForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )

    district_id = SelectField(
        u'District',
        validators=[
            DataRequired()
        ]
    )

    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')