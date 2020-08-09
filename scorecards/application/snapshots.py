from flask import Blueprint, render_template
from .scorecards import District
from .scorecards import SnapshotSummary
from .scorecards import DataCache
from .scorecards.Snapshots import PPESnapshot, StaffSnapshot, SpaceSnapshot, TransSnapshot, GeoSnapshot
from . import cache

# Blueprint Configuration
snap_bp = Blueprint(
    'snap_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
snap_templates={
    'summary':{
        'class':SnapshotSummary,
        'template':'summary_snapshot.html'
    },
    'ppe': {
        'class': PPESnapshot,
        'template': 'ppe_snapshot.html'
    },
    'space': {
        'class': SpaceSnapshot,
        'template': 'space_snapshot.html'
    },
    'staff': {
        'class': StaffSnapshot,
        'template': 'staff_snapshot.html'
    },
    'trans': {
        'class': TransSnapshot,
        'template': 'trans_snapshot.html'
    },
    'geo': {
        'class': GeoSnapshot,
        'template': 'geo_snapshot.html'
    },

}

@snap_bp.route('/snapshot/<snap_type>/<district_id>')
def get_snapshot(snap_type='summary',district_id=115):
    dc = cache.get(district_id)
    if dc == None:
        dc = DataCache(District(district_id))
        cache.set(district_id,dc)
    snap = snap_templates[snap_type]['class'](dc)
    return render_template(snap_templates[snap_type]['template'], snap=snap.status())
