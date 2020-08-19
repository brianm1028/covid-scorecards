"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class RoomForm(FlaskForm):

    room_type_id = SelectField(u'Room Type', coerce=int, validators=[DataRequired()])
    facility_id = SelectField(u'Facility', validators=[DataRequired()])
    room_number = StringField(u'Room Number', validators=[DataRequired()])
    capacity = IntegerField(u'Capacity', validators=[DataRequired()])
    del_button = SubmitField('Delete Room')
    upd_button = SubmitField('Update Room')
    add_button = SubmitField('Add Room')

class RoomDemandForm(FlaskForm):

    room_type_id = SelectField(u'Room Type', coerce=int, validators=[DataRequired()])
    facility_id = SelectField(u'Facility', validators=[DataRequired()])
    demand = IntegerField(u'Seats Required',validators=[DataRequired()])
    del_button = SubmitField('Delete Demand')
    upd_button = SubmitField('Update Demand')
    add_button = SubmitField('Add Demand')


