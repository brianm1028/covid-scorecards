from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import StaffUpdateForm,StaffUpdateChangeForm
from ..DataCaches import DistrictDataCache
from ..models import StaffStatusView, StaffRole, StaffUpdate, Facility
from . import staff_bp
from .. import db
from .. import Permissions
from datetime import datetime
from sqlalchemy import and_

@staff_bp.route('/staff/status/<district_id>', methods=['GET'])
@login_required
def status(district_id):
    if Permissions.check(Permissions.DISTRICT_SPACE_MANAGER,session['perms'][district_id]):
        facility_list = [f.id for f in Facility.query.filter_by(district_id=district_id)]
        facilities = sorted(Facility.query.filter_by(district_id=district_id), key=lambda x: x.facility_name)
    else:
        facility_list = [f for f in session['perms'].keys() if Permissions.check(Permissions.FACILITY_SPACE_MANAGER,session['perms'][f])]
        facilities = sorted(Facility.query.filter(Facility.id.in_(facility_list)), key=lambda x: x.facility_name)
    role_types = sorted(StaffRole.query.all(), key=lambda x: x.role_type)

    staff_status = StaffStatusView.query.filter(StaffStatusView.facility_id.in_(facility_list))

    form = request.args.get('form')
    if form is None:
        form = StaffUpdateForm()
        form.role_type_id.choices = [(i.role_type_id,i.role_type) for i in role_types]
        form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]

    upd_forms=[]
    for i in staff_status:
        f = StaffUpdateChangeForm()
        f.facility_id.data = i.facility_id
        f.role_type_id.data = i.role_type_id
        f.available.data = i.available
        f.required.data = i.required

        upd_forms.append({
            'facility_name': i.facility_name,
            'role_type': i.role_type,
            'update_data': i.update_date,
            'form': f
        })



    return render_template('staff/status.html', data=DistrictDataCache(district_id),upd_forms=upd_forms,add_form=form,session=session)

@staff_bp.route('/staff/updates/<district_id>', methods=['GET'])
@login_required
def staff_form(district_id):
    form = request.args.get('form')
    if form is None:
        form = StaffUpdateForm()
        role_types = StaffRole.query.all()
        if Permissions.check(Permissions.DISTRICT_STAFF_MANAGER, session['perms'][district_id]):
            facilities = Facility.query.filter_by(district_id=district_id)
        else:
            facility_list = [f for f in session['perms'].keys() if
                             Permissions.check(Permissions.FACILITY_STAFF_MANAGER, session['perms'][f])]
            facilities = Facility.query.filter(Facility.id.in_(facility_list))
        form.staff_role_id.choices = [(i.id,i.role_type) for i in role_types]
        form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
    return render_template('staff/update.html', data=DistrictDataCache(district_id), form=form,session=session)

@staff_bp.route('/staff/updates/<district_id>', methods=['POST'])
@login_required
def staff_post(district_id):

    form = StaffUpdateForm()

    if form.update.data or form.add.data:
        upd = StaffUpdate(
            update_date=datetime.now(),
            role_type_id=form.role_type_id.data,
            facility_id=form.facility_id.data,
            required=form.required.data,
            available=form.available.data,
            recorder_id=current_user.id
        )
        db.session.add(upd)
    if form.delete.data:
        for upd in StaffUpdate.query.filter(and_(StaffUpdate.facility_id==form.facility_id.data,StaffUpdate.role_type_id==form.role_type_id.data)).all():
            db.session.delete(upd)
    db.session.commit()
    return redirect(url_for('staff_bp.status',district_id=district_id))
