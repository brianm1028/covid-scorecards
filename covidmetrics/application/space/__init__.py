from flask import Blueprint

# Blueprint Configuration
space_bp = Blueprint(
    'space_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from .manager import status, room_form, room_post, demand_form, demand_post