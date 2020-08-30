from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from ..DataCaches import DistrictDataCache
from . import trans_bp
from ..models import BusGroup
from .forms import BusGroupForm
from .. import db
from datetime import datetime

@trans_bp.route('/trans/status/<district_id>', methods=['GET'])
@login_required
def status(district_id):

    add_form = BusGroupForm()
    add_form.district_id.data=district_id

    upd_forms=[]
    for bg in BusGroup.query.filter(BusGroup.district_id==district_id):
        f = BusGroupForm()
        f.bus_group_id.data=bg.bus_group_id
        f.district_id.data=bg.district_id
        f.available.data=bg.available
        f.required.data=bg.required

        upd_forms.append({
            'description': bg.description,
            'update_date': bg.update_date,
            'form': f
        })

    return render_template('trans/status.html', data=DistrictDataCache(district_id), upd_forms=upd_forms,add_form=add_form,session=session )

@trans_bp.route('/trans/updates/<district_id>', methods=['POST'])
@login_required
def updates_post(district_id):

    form = BusGroupForm()

    if form.add.data:
        bg = BusGroup(description=form.description.data,
                      district_id=form.district_id.data,
                      available=form.available.data,
                      required=form.required.data,
                      update_date=datetime.now(),
                      recorder_id=current_user.id)
        db.session.add(bg)
    if form.update.data:
        bg = BusGroup.query.filter(BusGroup.bus_group_id==form.bus_group_id.data).first()
        bg.available=form.available.data
        bg.required=form.required.data
        bg.update_date=datetime.now()
        bg.recorder_id=current_user.id

    if form.delete.data:
        bg = BusGroup.query.filter(BusGroup.bus_group_id==form.bus_group_id.data).first()
        db.session.delete(bg)

    db.session.commit()
    return redirect(url_for('trans_bp.status',district_id=district_id))
