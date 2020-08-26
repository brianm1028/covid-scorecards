
from flask import Blueprint, render_template, session
from .. import cache
from covidmetrics.application.DataCaches.DistrictDataCache import DistrictDataCache
from .Snapshots import *
from covidmetrics.application.DataCaches import *

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
        'template':'snapshots/summary.html'
    },
    'ppe': {
        'class': PPESnapshot,
        'dc': PPEDataCache,
        'template': 'snapshots/ppe.html'
    },
    'space': {
        'class': SpaceSnapshot,
        'dc': SpaceDataCache,
        'template': 'snapshots/space.html'
    },
    'staff': {
        'class': StaffSnapshot,
        'dc': StaffDataCache,
        'template': 'snapshots/staff.html'
    },
    'trans': {
        'class': TransSnapshot,
        'dc': TransDataCache,
        'template': 'snapshots/trans.html'
    },
    'geo': {
        'class': GeoSnapshot,
        'dc': GeoDataCache,
        'template': 'snapshots/geo.html'
    },

}

@snap_bp.route('/snapshot/<snap_type>/<district_id>')
def get_snapshot(snap_type='summary',district_id='3404906700000'):
    ddc = cache.get('district' + str(district_id))
    if ddc is None:
        ddc = DistrictDataCache(district_id)
        cache.set('district' + str(district_id), ddc)

    session['district_id']=ddc.district_id
    session['district_name']=ddc.district_name
    print(session)

    dc = cache.get(snap_type + str(district_id))
    if dc is None:
        dc = snap_templates[snap_type]['dc'](dc=ddc)
        cache.set(snap_type + str(district_id),dc)
    snap = snap_templates[snap_type]['class'](dc)
    return render_template(snap_templates[snap_type]['template'], data=snap.status(), session=session)
