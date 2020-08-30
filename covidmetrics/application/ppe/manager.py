from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import TransactionForm, UpdatePPEForm
from ..models import PPETransaction, PPEItem, Facility, PPETransactionsView, PPEInventoryView
from .. import Permissions
from ..DataCaches import DistrictDataCache
from .. import db
from . import ppe_bp
from datetime import datetime
from sqlalchemy import and_

@ppe_bp.route('/ppe/transaction/history/<district_id>', methods=['GET'])
@login_required
def history(district_id):
    if Permissions.check(Permissions.DISTRICT_PPE_MANAGER,session['perms'][district_id]):
        facility_list = [f.id for f in Facility.query.filter_by(district_id=district_id)]
    else:
        facility_list = [f for f in session['perms'].keys() if Permissions.check(Permissions.FACILITY_PPE_MANAGER,session['perms'][f])]
    transactions = PPETransactionsView.query.filter(PPETransactionsView.facility_id.in_(facility_list))
    return render_template('ppe/history.html', data=DistrictDataCache(district_id), ppe_transactions=transactions,session=session)

@ppe_bp.route('/ppe/status/<district_id>', methods=['GET'])
@login_required
def status(district_id):
    if Permissions.check(Permissions.DISTRICT_PPE_MANAGER,session['perms'][district_id]):
        facility_list = [f.id for f in Facility.query.filter_by(district_id=district_id)]
    else:
        facility_list = [f for f in session['perms'].keys() if Permissions.check(Permissions.FACILITY_PPE_MANAGER,session['perms'][f])]
    ppe_inventory = PPEInventoryView.query.filter(PPEInventoryView.facility_id.in_(facility_list))
    form = request.args.get('form')
    if form is None:
        form = TransactionForm()
        ppe_items = PPEItem.query.all()
        facilities = sorted(Facility.query.filter(Facility.id.in_(facility_list)), key=lambda x: x.facility_name)
        form.ppe_item_id.choices = [(i.id,i.description) for i in ppe_items]
        form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
    upd_forms=[]
    for i in ppe_inventory:
        f = UpdatePPEForm()
        f.ppe_item_id.data=i.ppe_item_id
        f.facility_id.data=i.facility_id
        f.quantity.data=i.quantity
        f.prior_quantity.data = i.quantity

        upd_forms.append({
            'facility_name': i.facility_name,
            'description': i.description,
            'quantity': i.quantity,
            'update_date': i.update_date,
            'form': f
        })
    return render_template('ppe/status.html', data=DistrictDataCache(district_id), upd_forms=upd_forms, add_form=form,session=session)



@ppe_bp.route('/ppe/transaction/<district_id>', methods=['GET'])
@login_required
def transaction_form(district_id):
    if Permissions.check(Permissions.DISTRICT_PPE_MANAGER,session['perms'][district_id]):
        facility_list = [f.id for f in Facility.query.filter_by(district_id=district_id)]
    else:
        facility_list = [f for f in session['perms'].keys() if Permissions.check(Permissions.FACILITY_PPE_MANAGER,session['perms'][f])]
    form = request.args.get('form')
    if form is None:
        form = TransactionForm()
        ppe_items = PPEItem.query.all()
        facilities = sorted(Facility.query.filter(Facility.id.in_(facility_list)), key=lambda x: x.facility_name)
        form.ppe_item_id.choices = [(i.id,i.description) for i in ppe_items]
        form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
    return render_template('ppe/transaction.html', data=DistrictDataCache(district_id), form=form,session=session)

@ppe_bp.route('/ppe/transaction/<district_id>', methods=['POST'])
@login_required
def transaction_post(district_id):

    form = TransactionForm()

    quantity = int(form.quantity.data)
    if form.add.data:
        ppe_tx = PPETransaction(date=datetime.now(),
                                ppe_item_id=form.ppe_item_id.data,
                                facility_id=form.facility_id.data,
                                quantity=quantity,
                                recorder_id=current_user.id)
        db.session.add(ppe_tx)
        db.session.commit()
    if form.subtract.data:
        ppe_tx = PPETransaction(date=datetime.now(),
                                ppe_item_id=form.ppe_item_id.data,
                                facility_id=form.facility_id.data,
                                quantity=quantity*-1,
                                recorder_id=current_user.id)
        db.session.add(ppe_tx)
        db.session.commit()
    if form.update.data:
        ppe_tx = PPETransaction(date=datetime.now(),
                                ppe_item_id=form.ppe_item_id.data,
                                facility_id=form.facility_id.data,
                                quantity=quantity-int(form.prior_quantity.data),
                                recorder_id=current_user.id)
        db.session.add(ppe_tx)
        db.session.commit()

    if form.delete.data:
        for t in PPETransaction.query.filter(and_(
            PPETransaction.ppe_item_id==form.ppe_item_id.data,
            PPETransaction.facility_id==form.facility_id.data
        )):
            db.session.delete(t)
        db.session.commit()
    return redirect(url_for('ppe_bp.status',district_id=district_id))
