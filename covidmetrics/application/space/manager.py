from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import RoomForm, RoomDemandForm
from ..models import SpaceStatusView, Room, RoomType, RoomDemand, Facility
from ..DataCaches import DistrictDataCache
from .. import db
from . import space_bp

@space_bp.route('/space/status/<district_id>', methods=['GET'])
@login_required
def status(district_id):
    status = SpaceStatusView.query.all()
    return render_template('space/status.html', data=DistrictDataCache(district_id), status=status,session=session)

@space_bp.route('/space/rooms/<district_id>', methods=['GET'])
@login_required
def room_form(district_id):
    form = request.args.get('form')
    if form is None:
        form = RoomForm()
        room_types = RoomType.query.all()
        facilities = Facility.query.all()
        form.room_type_id.choices = [(i.id,i.description) for i in room_types]
        form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
    return render_template('space/room.html', data=DistrictDataCache(district_id), form=form,session=session)

@space_bp.route('/space/rooms/<district_id>', methods=['POST'])
@login_required
def room_post(district_id):

    form = RoomForm()

    room_tx = Room(room_type_id=form.room_type_id.data,
                   facility_id=form.facility_id.data,
                   room_number=form.room_number.data,
                   capacity=form.capacity.data,
                   recorder_id=current_user.id)
    db.session.add(room_tx)
    db.session.commit()
    return redirect(url_for('space_bp.status',district_id=district_id))

@space_bp.route('/space/demand/<district_id>', methods=['GET'])
@login_required
def demand_form(district_id):
    form = request.args.get('form')
    if form is None:
        form = RoomDemandForm()
        room_types = RoomType.query.all()
        facilities = Facility.query.all()
        form.room_type_id.choices = [(i.id,i.description) for i in room_types]
        form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
    return render_template('space/demand.html', data=DistrictDataCache(district_id), form=form,session=session)

@space_bp.route('/space/demand/<district_id>', methods=['POST'])
@login_required
def demand_post(district_id):

    form = RoomDemandForm()

    demand_tx = RoomDemand(room_type_id=form.room_type_id.data,
                   facility_id=form.facility_id.data,
                   demand=form.demand.data,
                   recorder_id=current_user.id)
    db.session.add(demand_tx)
    db.session.commit()
    return redirect(url_for('space_bp.status', district_id=district_id))
