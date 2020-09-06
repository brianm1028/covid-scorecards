from .. import db

class UserFacilityRole(db.Model):
    __tablename__ = 'user_facility_roles'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.String, db.ForeignKey("facilities.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("user_roles.role_id"))
    update_date = db.Column(db.DateTime)
    recorder_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def __init__(self, facility_id, user_id, role_id,update_date,recorder_id):
        self.facility_id = facility_id
        self.user_id = user_id
        self.role_id = role_id
        self.update_date=update_date
        self.recorder_id=recorder_id

    def __repr__(self):
        return '<UserFacilityRole %r>' % (str(self.id))
