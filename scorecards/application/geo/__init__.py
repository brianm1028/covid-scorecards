from flask import Blueprint

# Blueprint Configuration
geo_bp = Blueprint(
    'geo_bp', __name__,
    template_folder='templates',
    static_folder='static'
)