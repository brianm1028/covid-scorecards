"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class TransactionForm(FlaskForm):
    """User Sign-up Form."""

    ppe_item_id = SelectField(u'PPE Item', coerce=int, validators=[DataRequired()])

    facility_id = SelectField(u'Facility', validators=[DataRequired()])

    prior_quantity = HiddenField(u'Prior Quantity')

    quantity = IntegerField(
        'Quantity',
        validators=[
            DataRequired()
        ]
    )

    add = SubmitField('Add')
    subtract = SubmitField('Sub')
    update = SubmitField('Save')
    delete = SubmitField('Del')

class UpdatePPEForm(TransactionForm):
    """User Sign-up Form."""

    ppe_item_id = HiddenField(u'PPE Item', validators=[DataRequired()])

    facility_id = HiddenField(u'Facility', validators=[DataRequired()])

    prior_quantity = HiddenField(u'Prior Quantity')




