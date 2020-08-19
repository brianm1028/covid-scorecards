from flask import Blueprint

# Blueprint Configuration
trans_bp = Blueprint(
    'trans_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from .manager import status