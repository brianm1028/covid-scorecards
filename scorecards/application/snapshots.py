from flask import Blueprint, render_template
from .scorecards import District
from .scorecards.Snapshots import SummarySnapshot, PPESnapshot, StaffSnapshot, SpaceSnapshot, TransSnapshot, GeoSnapshot
from .scorecards.DataCaches import SummaryDataCache, PPEDataCache, StaffDataCache, SpaceDataCache, TransDataCache, GeoDataCache
from . import cache

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
        'template':'summary_snapshot.html'
    },
    'ppe': {
        'class': PPESnapshot,
        'dc': PPEDataCache,
        'template': 'ppe_snapshot.html'
    },
    'space': {
        'class': SpaceSnapshot,
        'dc': SpaceDataCache,
        'template': 'space_snapshot.html'
    },
    'staff': {
        'class': StaffSnapshot,
        'dc': StaffDataCache,
        'template': 'staff_snapshot.html'
    },
    'trans': {
        'class': TransSnapshot,
        'dc': TransDataCache,
        'template': 'trans_snapshot.html'
    },
    'geo': {
        'class': GeoSnapshot,
        'dc': GeoDataCache,
        'template': 'geo_snapshot.html'
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
