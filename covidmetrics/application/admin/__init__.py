from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .. import cache
from ..DataCaches import DistrictDataCache

# Blueprint Configuration
admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@admin_bp.route('/admin/<district_id>')
@login_required
def admin_index(district_id='3404906700000'):
#    ddc = cache.get('district' + str(district_id))
#    if ddc is None:
#        ddc = DistrictDataCache(district_id)
#        cache.set('district' + str(district_id), ddc)

    return render_template('admin/index.html', data=DistrictDataCache(district_id))

@admin_bp.route('/admin/<section>/<district_id>')
@login_required
def district_config(section='district', district_id='3404906700000'):
#    ddc = cache.get('district' + str(district_id))
#    if ddc is None:
#        ddc = DistrictDataCache(district_id)
#        cache.set('district' + str(district_id), ddc)

    return render_template('admin/'+section+'_config.html', data=DistrictDataCache(district_id))
