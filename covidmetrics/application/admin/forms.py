"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField, IntegerField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class DistrictConfigForm(FlaskForm):
    """User Sign-up Form."""


    enabled = BooleanField()

    update = SubmitField('Save')

class GeoConfigForm(FlaskForm):

    enabled = BooleanField()

    disp_region = BooleanField()
    region_duration = IntegerField()
    region_threshold = DecimalField()

    disp_county = BooleanField()
    county_duration = IntegerField()
    county_threshold = DecimalField()

    disp_zip = BooleanField()
    zip_duration = IntegerField()
    zip_threshold = DecimalField()

    disp_county_inc = BooleanField()
    county_inc_average = IntegerField()
    county_inc_duration = IntegerField()
    county_inc_hyb_threshold = IntegerField()
    county_inc_inp_threshold = IntegerField()

    disp_county_cli = BooleanField()
    county_cli_duration = IntegerField()
    county_cli_hyb_threshold = IntegerField()
    county_cli_inp_threshold = IntegerField()

    disp_county_tat = BooleanField()
    county_tat_duration = IntegerField()
    county_tat_hyb_threshold = IntegerField()
    county_tat_inp_threshold = IntegerField()

    update = SubmitField('Save')

class PPEConfigForm(FlaskForm):
    enabled = BooleanField()
    update = SubmitField('Save')

class SpaceConfigForm(FlaskForm):
    enabled = BooleanField()
    update = SubmitField('Save')

class StaffConfigForm(FlaskForm):
    enabled = BooleanField()
    update = SubmitField('Save')

class TransConfigForm(FlaskForm):
    enabled = BooleanField()
    update = SubmitField('Save')

class DistrictRoleForm(FlaskForm):
    scope = HiddenField()
    user_id = SelectField('User')
    role_id = SelectField('Role')

    delete = SubmitField('Del')
    update = SubmitField('Save')
    add = SubmitField('Add')

class FacilityRoleForm(FlaskForm):
    scope = HiddenField()
    user_id = SelectField('User')
    facility_id = SelectField('Facility')
    role_id = SelectField('Role')

    delete = SubmitField('Del')
    update = SubmitField('Save')
    add = SubmitField('Add')


class DistrictRoleUpdateForm(DistrictRoleForm):
    id = HiddenField()

class FacilityRoleUpdateForm(FacilityRoleForm):
    id = HiddenField()

