from flask import Blueprint

# Blueprint Configuration
ppe_bp = Blueprint(
    'ppe_bp', __name__,
    template_folder='templates',
    static_folder='static'
)