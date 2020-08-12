from flask import Blueprint

# Blueprint Configuration
admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates',
    static_folder='static'
)