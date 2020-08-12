
from flask import Blueprint, render_template
from .. import cache
from ..District import District
from .Snapshots import *
from .DataCaches import *

# Blueprint Configuration
snap_bp = Blueprint(
    'snap_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
snap_templates={
    'summary':{
        'class': SummarySnapshot,
        'dc': SummaryDataCache,
        'template':'summary.html'
    },
    'ppe': {
        'class': PPESnapshot,
        'dc': PPEDataCache,
        'template': 'ppe.html'
    },
    'space': {
        'class': SpaceSnapshot,
        'dc': SpaceDataCache,
        'template': 'space.html'
    },
    'staff': {
        'class': StaffSnapshot,
        'dc': StaffDataCache,
        'template': 'staff.html'
    },
    'trans': {
        'class': TransSnapshot,
        'dc': TransDataCache,
        'template': 'trans.html'
    },
    'geo': {
        'class': GeoSnapshot,
        'dc': GeoDataCache,
        'template': 'geo.html'
    },

}

@snap_bp.route('/snapshot/<snap_type>/<district_id>')
def get_snapshot(snap_type='summary',district_id=115):
    dc = cache.get(snap_type + str(district_id))
    if dc is None:
        dc = snap_templates[snap_type]['dc'](District(district_id))
        cache.set(snap_type + str(district_id),dc)
    snap = snap_templates[snap_type]['class'](dc)
    return render_template(snap_templates[snap_type]['template'], snap=snap.status())
