from flask import Blueprint

# Blueprint Configuration
staff_bp = Blueprint(
    'staff_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from .manager import status