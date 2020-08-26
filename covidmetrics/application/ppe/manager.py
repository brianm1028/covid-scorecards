from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import TransactionForm
from ..models import PPETransaction, PPEItem, Facility, PPETransactionsView, PPEInventoryView
from ..DataCaches import DistrictDataCache
from .. import db
from . import ppe_bp

@ppe_bp.route('/ppe/transaction/history/<district_id>', methods=['GET'])
@login_required
def history(district_id):
    transactions = PPETransactionsView.query.all()
    return render_template('ppe/history.html', data=DistrictDataCache(district_id), ppe_transactions=transactions,session=session)

@ppe_bp.route('/ppe/status/<district_id>', methods=['GET'])
@login_required
def status(district_id):
    ppe_inventory = PPEInventoryView.query.all()
    return render_template('ppe/status.html', data=DistrictDataCache(district_id), ppe_inventory=ppe_inventory,session=session)



@ppe_bp.route('/ppe/transaction/<district_id>', methods=['GET'])
@login_required
def transaction_form(district_id):
    form = request.args.get('form')
    if form is None:
        form = TransactionForm()
        ppe_items = PPEItem.query.all()
        facilities = Facility.query.all()
        form.ppe_item_id.choices = [(i.id,i.description) for i in ppe_items]
        form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
    return render_template('ppe/transaction.html', data=DistrictDataCache(district_id), form=form,session=session)

@ppe_bp.route('/ppe/transaction/<district_id>', methods=['POST'])
@login_required
def transaction_post(district_id):

    form = TransactionForm()

    if form.transaction_type=='sub':
        quantity = form.quantity.data * -1
    else:
        quantity = form.quantity.data
    ppe_tx = PPETransaction(ppe_item_id=form.ppe_item_id.data,
                            facility_id=form.facility_id.data,
                            quantity=quantity,
                            recorder_id=current_user.id)
    db.session.add(ppe_tx)
    db.session.commit()
    return redirect(url_for('ppe_bp.history',district_id=district_id))
