from flask import Blueprint

# Blueprint Configuration
space_bp = Blueprint(
    'space_bp', __name__,
    template_folder='templates',
    static_folder='static'
)