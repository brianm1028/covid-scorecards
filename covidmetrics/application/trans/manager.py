from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from ..DataCaches import DistrictDataCache
from . import trans_bp

@trans_bp.route('/trans/status/<district_id>', methods=['GET'])
@login_required
def status(district_id):
    return render_template('trans/status.html', data=DistrictDataCache(district_id) )
