from flask import Blueprint, render_template
from .scorecards import District
from .scorecards import SnapshotSummary
from .scorecards import PPESnapshot, StaffSnapshot, SpaceSnapshot, TransSnapshot, GeoSnapshot


# Blueprint Configuration
snap_bp = Blueprint(
    'snap_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@snap_bp.route('/snapshot/<district_id>')
def get_summary_snapshot(district_id):
    snap = SnapshotSummary(District(district_id))
    return render_template('summary_snapshot.html', snap=snap.status())


# TODO consolidate get_<type>_snapshot methods using path parameter
# TODO implement SnapshotFactory class
@snap_bp.route('/snapshot/ppe/<district_id>')
def get_ppe_snapshot(district_id):
    snap = PPESnapshot(District(district_id))
    return render_template('ppe_snapshot.html', snap=snap.status())


@snap_bp.route('/snapshot/staff/<district_id>')
def get_staff_snapshot(district_id):
    snap = StaffSnapshot(District(district_id))
    return render_template('staff_snapshot.html', snap=snap.status())


@snap_bp.route('/snapshot/space/<district_id>')
def get_space_snapshot(district_id):
    snap = SpaceSnapshot(District(district_id))
    return render_template('space_snapshot.html', snap=snap.status())


@snap_bp.route('/snapshot/trans/<district_id>')
def get_trans_snapshot(district_id):
    snap = TransSnapshot(District(district_id))
    return render_template('trans_snapshot.html', snap=snap.status())


@snap_bp.route('/snapshot/geo/<district_id>')
def get_geo_snapshot(district_id):
    snap = GeoSnapshot(District(district_id))
    return render_template('geo_snapshot.html', snap=snap.status())
