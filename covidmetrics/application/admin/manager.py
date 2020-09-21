from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import DistrictConfigForm, GeoConfigForm, PPEConfigForm, SpaceConfigForm, StaffConfigForm, TransConfigForm, DistrictRoleForm, FacilityRoleForm, DistrictRoleUpdateForm, FacilityRoleUpdateForm
from sqlalchemy.orm.attributes import flag_modified
from ..models import Configuration, Facility, UserRole, UserDistrict, UserDistrictView, UserDistrictRole, UserFacilityRole
from .. import Permissions
from ..DataCaches import DistrictDataCache
from .. import db
from . import admin_bp
from datetime import datetime
from sqlalchemy import and_

admin_templates={
    'geo':{
        'form':GeoConfigForm
    },
    'ppe':{
        'form':PPEConfigForm
    },
    'space':{
        'form':SpaceConfigForm
    },
    'staff':{
        'form':StaffConfigForm
    },
    'trans':{
        'form':TransConfigForm
    },
    'users':{
        'district':DistrictRoleUpdateForm,
        'facility':FacilityRoleUpdateForm
    }
}

@admin_bp.route('/admin/<section>/<district_id>', methods=['GET'])
@login_required
def section_admin_form(section,district_id):

    if section=="users":
        facility_list = [f.id for f in Facility.query.filter_by(district_id=district_id)]
        facilities = sorted(Facility.query.filter_by(district_id=district_id), key=lambda x: x.facility_name)
        district_users = UserDistrictView.query.filter_by(district_id=district_id).all()

        user_roles = UserRole.query.filter(UserRole.permset < Permissions.SITE_ADMIN)
        district_user_roles = [ur for ur in user_roles if Permissions.check(Permissions.DISTRICT,ur.permset)]
        facility_user_roles = [ur for ur in user_roles if not Permissions.check(Permissions.DISTRICT,ur.permset)]

        new_district_user_form = DistrictRoleForm()
        new_district_user_form.scope.data = 'district'
        new_district_user_form.role_id.choices = [(i.role_id,i.description) for i in district_user_roles]
        new_district_user_form.user_id.choices = [(i.user_id,i.user_name) for i in district_users]

        new_facility_user_form = FacilityRoleForm()
        new_facility_user_form.scope.data='facility'
        new_facility_user_form.role_id.choices = [(i.role_id,i.description) for i in facility_user_roles]
        new_facility_user_form.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
        new_facility_user_form.user_id.choices = [(i.user_id,i.user_name) for i in district_users]

        user_district_roles = UserDistrictRole.query.filter_by(district_id=district_id).all()
        user_facility_roles = UserFacilityRole.query.filter(UserFacilityRole.facility_id.in_(facility_list)).all()

        forms={}
        forms['new_facility_user_form']=new_facility_user_form
        forms['new_district_user_form']=new_district_user_form
        forms['district_user_forms']=[]
        forms['facility_user_forms']=[]
        for udr in user_district_roles:
            f = DistrictRoleUpdateForm()
            f.id.data=udr.id
            f.scope.data='district'
            f.user_id.choices = [(i.user_id,i.user_name) for i in district_users]
            f.user_id.data=str(udr.user_id)
            f.role_id.choices = [(i.role_id,i.description) for i in district_user_roles]
            f.role_id.data=str(udr.role_id)
            forms['district_user_forms'].append(f)

        for ufr in user_facility_roles:
            f = FacilityRoleUpdateForm()
            f.id.data=ufr.id
            f.scope.data='facility'
            f.user_id.choices = [(i.user_id,i.user_name) for i in district_users]
            f.user_id.data=str(ufr.user_id)
            f.role_id.choices = [(i.role_id,i.description) for i in facility_user_roles]
            f.role_id.data=str(ufr.role_id)
            f.facility_id.choices = [(i.id,i.facility_name) for i in facilities]
            f.facility_id.data=ufr.facility_id
            forms['facility_user_forms'].append(f)

        return render_template('admin/' + section + '_config.html', data=DistrictDataCache(district_id), forms=forms,session=session)

    else:

        form = request.args.get('form')
        if form is None:
            dist = Configuration.query.filter(Configuration.district_id==district_id).first()
            form = admin_templates[section]['form']()
            for f in dist.configuration[section].keys():
                if f in form:
                    form[f].data = dist.configuration[section][f]
        return render_template('admin/'+section+'_config.html', data=DistrictDataCache(district_id), form=form, session=session)

@admin_bp.route('/admin/<section>/<district_id>', methods=['POST'])
@login_required
def section_admin_post(section,district_id):
    if section == "users":

        form = admin_templates[section][request.form['scope']]()

        if form.add.data:
            if form.scope.data=='district':
                u = UserDistrictRole(
                    district_id=district_id,
                    user_id=int(form.user_id.data),
                    role_id=int(form.role_id.data),
                    update_date=datetime.now(),
                    recorder_id=current_user.id
                )
            else:
                u = UserFacilityRole(
                    user_id=int(form.user_id.data),
                    role_id=int(form.role_id.data),
                    facility_id=form.facility_id.data,
                    update_date=datetime.now(),
                    recorder_id=current_user.id
                )
            db.session.add(u)
            db.session.commit()
        if form.update.data:
            if form.scope.data=='district':
                u = UserDistrictRole.query.filter_by(id=form.id.data).first()
                u.user_id = int(form.user_id.data)
                u.role_id = int(form.role_id.data)
                u.update_date = datetime.now()
                u.recorder_id = current_user.id
            else:
                u = UserFacilityRole.query.filter_by(id=form.id.data).first()
                u.user_id = int(form.user_id.data)
                u.role_id = int(form.role_id.data)
                u.facility_id = form.facility_id.data
                u.update_date = datetime.now()
                u.recorder_id = current_user.id

            db.session.commit()

        if form.delete.data:
            if form.scope.data=='district':
                u = UserDistrictRole.query.filter_by(id=int(form.id.data)).first()
            else:
                u = UserFacilityRole.query.filter_by(id=int(form.id.data)).first()
            db.session.delete(u)
            db.session.commit()

        return redirect(
            url_for('admin_bp.section_admin_form', section=section, district_id=district_id))

    else:

        form = admin_templates[section]['form']()

        if form.update.data:
            dist = Configuration.query.filter(Configuration.district_id==district_id).first()
            # update fields in dist_conf
            for f in dist.configuration[section].keys():
                if f in form:
                    dist.configuration[section][f]=form[f].data
            flag_modified(dist,"configuration")
            dist.update_date=datetime.now()
            dist.recorder_id=current_user.id
            db.session.commit()
        return redirect(url_for('admin_bp.section_admin_form',section=section,district_id=district_id))


@admin_bp.route('/admin/<district_id>', methods=['GET'])
@login_required
def district_admin_form(district_id):
    form = request.args.get('form')
    if form is None:
        dist = Configuration.query.filter(Configuration.district_id==district_id).first()
        form = DistrictConfigForm()
        form.enabled.data = dist.configuration['enabled']
    return render_template('admin/district_config.html', data=DistrictDataCache(district_id), form=form,session=session)

@admin_bp.route('/admin/<district_id>', methods=['POST'])
@login_required
def district_admin_post(district_id):

    form = DistrictConfigForm()

    if form.update.data:
        dist = Configuration.query.filter(Configuration.district_id==district_id).first()
        # update fields in dist_conf
        dist.configuration['enabled']=form.enabled.data
        flag_modified(dist,"configuration")
        dist.update_date=datetime.now()
        dist.recorder_id=current_user.id
        db.session.commit()
    return redirect(url_for('admin_bp.district_admin_form',district_id=district_id,session=session))
