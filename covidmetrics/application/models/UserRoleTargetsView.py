from .. import db

class UserRoleTargetsView(db.Model):
    __tablename__ = 'user_role_targets_vw'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    user_name = db.Column(db.String)
    target_id = db.Column(db.String, primary_key=True)
    target_name = db.Column(db.String)
    target_type = db.Column(db.String)
    district_id = db.Column(db.String, db.ForeignKey('districts.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.role_id'), primary_key=True)
    role_description = db.Column(db.String)
    permset = db.Column(db.Integer)

    def __init__(self, user_id, user_name, target_id, target_name, target_type, district_id, role_id, role_description, permset):
        self.user_id=user_id
        self.user_name = user_name
        self.target_id=target_id
        self.target_name=target_name
        self.target_type=target_type
        self.district_id=district_id
        self.role_id=role_id
        self.role_description=role_description
        self.permset=permset

    def __repr__(self):
        return '<UserRoleTargetsView %r>' % (self.user_name +'-'+self.role_description+'@'+self.facility_name)
