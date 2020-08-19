"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class TransactionForm(FlaskForm):
    """User Sign-up Form."""

    ppe_item_id = SelectField(u'PPE Item', coerce=int, validators=[DataRequired()])

    facility_id = SelectField(u'Facility', validators=[DataRequired()])

    transaction_type = RadioField(
        u'Type of Transaction',
        choices=[('add','Add to Inventory'),('sub','Subtract from Inventory')],
        validators = [DataRequired()]
    )
    quantity = IntegerField(
        'Quantity',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Add Transaction')

