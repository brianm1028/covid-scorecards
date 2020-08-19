from flask import Blueprint
from ..DataCaches import DistrictDataCache

# Blueprint Configuration
ppe_bp = Blueprint(
    'ppe_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from .manager import history, status, transaction_form, transaction_post