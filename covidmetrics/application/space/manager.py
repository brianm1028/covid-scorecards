from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import RoomForm, RoomDemandForm, RoomUpdateForm, RoomDemandUpdateForm
from ..models import SpaceStatusView, Room, RoomType, RoomDemand, Facility
from ..DataCaches import DistrictDataCache
from .. import Permissions
from .. import db
from . import space_bp
from datetime import datetime
from sqlalchemy import and_

@space_bp.route('/space/status/<district_id>', methods=['GET'])
@login_required
def status(district_id):
    if Permissions.check(Permissions.DISTRICT_SPACE_MANAGER,session['perms'][district_id]):
        facility_list = [f.id for f in Facility.query.filter_by(district_id=district_id)]
        facilities = sorted(Facility.query.filter_by(district_id=district_id), key=lambda x: x.facility_name)
    else:
        facility_list = [f for f in session['perms'].keys() if Permissions.check(Permissions.FACILITY_SPACE_MANAGER,session['perms'][f])]
        facilities = sorted(Facility.query.filter(Facility.id.in_(facility_list)), key=lambda x: x.facility_name)
    room_types = sorted(RoomType.query.all(), key=lambda x: x.description)

    data={
        'facilities': {}
    }

    data['room_form'] = RoomForm()
    data['room_form'].room_type_id.choices = [(i.id, i.description) for i in room_types]
    data['room_form'].facility_id.choices = [(i.id, i.facility_name) for i in facilities]

    data['demand_form'] = RoomDemandForm()
    data['demand_form'].room_type_id.choices = [(i.id, i.description) for i in room_types]
    data['demand_form'].facility_id.choices = [(i.id, i.facility_name) for i in facilities]

    for sv in sorted(SpaceStatusView.query.filter(SpaceStatusView.facility_id.in_(facility_list)), key=lambda x: x.facility_name):
        if sv.facility_id not in data['facilities'].keys():
            data['facilities'][sv.facility_id]={
                'facility_name': sv.facility_name,
                'room_types': {}
            }
        if sv.room_type_id not in data['facilities'][sv.facility_id]['room_types'].keys():
            data['facilities'][sv.facility_id]['room_types'][sv.room_type_id]={
                'available':sv.available,
                'required':sv.required,
                'description':sv.description,
                'rooms':[]
            }

        for r in Room.query.filter(and_(Room.facility_id==sv.facility_id,Room.room_type_id==sv.room_type_id)):
            form = RoomUpdateForm()
            form.room_id.data = r.id
            form.capacity.data = r.capacity
            data['facilities'][sv.facility_id]['room_types'][sv.room_type_id]['rooms'].append({
                'room_number': r.room_number,
                'form': form
            })

        form = RoomDemandUpdateForm()
        form.room_type_id.data = sv.room_type_id
        form.facility_id.data = sv.facility_id
        d = RoomDemand.query.filter(and_(RoomDemand.facility_id==sv.facility_id,RoomDemand.room_type_id==sv.room_type_id)).first()
        if d:
            form.room_demand_id.data=d.id
            form.demand.data = d.demand
        else:
            form.room_demand_id.data=0
            form.demand.data=0
        data['facilities'][sv.facility_id]['room_types'][sv.room_type_id]['demand'] = form.demand.data
        data['facilities'][sv.facility_id]['room_types'][sv.room_type_id]['demand_form'] = form

    return render_template('space/status.html', data=DistrictDataCache(district_id), status=data, session=session)

@space_bp.route('/space/rooms/<district_id>', methods=['GET'])
@login_required
def room_form(district_id):
    form = request.args.get('form')
    if form is None:
        form = RoomForm()
        if Permissions.check(Permissions.DISTRICT_SPACE_MANAGER, session['perms'][district_id]):
            facility_list = [f.id for f in Facility.query.filter_by(district_id=district_id)]
            facilities = sorted(Facility.query.filter_by(district_id=district_id), key=lambda x: x.facility_name)
        else:
            facility_list = [f for f in session['perms'].keys() if
                             Permissions.check(Permissions.FACILITY_SPACE_MANAGER, session['perms'][f])]
            facilities = sorted(Facility.query.filter(Facility.id.in_(facility_list)), key=lambda x: x.facility_name)
        room_types = sorted(RoomType.query.all(), key=lambda x: x.description)
        form.room_type_id.choices = [(i.id,i.description) for i in room_types]
        form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
    return render_template('space/room.html', data=DistrictDataCache(district_id), form=form,session=session)

@space_bp.route('/space/rooms/<district_id>', methods=['POST'])
@login_required
def room_post(district_id):

    form = RoomForm()

    room_tx = Room(update_date=datetime.now(),
                   room_type_id=form.room_type_id.data,
                   facility_id=form.facility_id.data,
                   room_number=form.room_number.data,
                   capacity=form.capacity.data,
                   recorder_id=current_user.id)
    db.session.add(room_tx)
    db.session.commit()
    return redirect(url_for('space_bp.status',district_id=district_id))

@space_bp.route('/space/rooms/update/<district_id>', methods=['POST'])
@login_required
def room_update(district_id):

    form = RoomUpdateForm()
    r = Room.query.filter(Room.id == form.room_id.data).first()
    if form.update.data:
        r.capacity=form.capacity.data
        r.update_date=datetime.now()
        r.recorder_id=current_user.id
        #db.session.update(r)
    if form.delete.data:
        db.session.delete(r)
    db.session.commit()
    return redirect(url_for('space_bp.status',district_id=district_id))

@space_bp.route('/space/demand/<district_id>', methods=['GET'])
@login_required
def demand_form(district_id):
    form = request.args.get('form')
    if form is None:
        form = RoomDemandForm()
        if Permissions.check(Permissions.DISTRICT_SPACE_MANAGER, session['perms'][district_id]):
            facility_list = [f.id for f in Facility.query.filter_by(district_id=district_id)]
            facilities = sorted(Facility.query.filter_by(district_id=district_id), key=lambda x: x.facility_name)
        else:
            facility_list = [f for f in session['perms'].keys() if
                             Permissions.check(Permissions.FACILITY_SPACE_MANAGER, session['perms'][f])]
            facilities = sorted(Facility.query.filter(Facility.id.in_(facility_list)), key=lambda x: x.facility_name)
        room_types = sorted(RoomType.query.all(), key=lambda x: x.description)
        form.room_type_id.choices = [(i.id,i.description) for i in room_types]
        form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
    return render_template('space/demand.html', data=DistrictDataCache(district_id), form=form,session=session)

@space_bp.route('/space/demand/<district_id>', methods=['POST'])
@login_required
def demand_post(district_id):

    form = RoomDemandForm()

    demand_tx = RoomDemand(
        update_date=datetime.now(),
        room_type_id=form.room_type_id.data,
                   facility_id=form.facility_id.data,
                   demand=form.demand.data,
                   recorder_id=current_user.id)
    db.session.add(demand_tx)
    db.session.commit()
    return redirect(url_for('space_bp.status', district_id=district_id))

@space_bp.route('/space/demand/update/<district_id>', methods=['POST'])
@login_required
def demand_update(district_id):

    form = RoomDemandUpdateForm()
    if form.room_demand_id==0:
        rd = RoomDemand(
            room_type_id=form.room_type_id.data,
            facility_id=form.facility_id.data,
            demand=form.demand.data,
            recorder_id=current_user.id,
            update_date=datetime.now())
        db.session.add(rd)
    else:
        rd = RoomDemand.query.filter(RoomDemand.id == form.room_demand_id.data).first()
        if form.update.data:
            rd.demand=form.demand.data
            rd.update_date=datetime.now()
            rd.recorder_id=current_user.id
            #db.session.update(rd)
        if form.delete.data:
            db.session.delete(rd)
    db.session.commit()
    return redirect(url_for('space_bp.status', district_id=district_id))