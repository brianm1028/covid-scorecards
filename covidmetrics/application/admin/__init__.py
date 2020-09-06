from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from .. import cache
from ..DataCaches import DistrictDataCache

# Blueprint Configuration
admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from .manager import section_admin_form, section_admin_post, district_admin_form, district_admin_post