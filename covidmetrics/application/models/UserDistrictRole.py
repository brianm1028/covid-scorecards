from .. import db

class UserDistrictRole(db.Model):
    __tablename__ = 'user_district_roles'
    id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.String, db.ForeignKey("districts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("user_roles.role_id"))
    update_date = db.Column(db.DateTime)
    recorder_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, district_id, user_id, role_id,update_date,recorder_id):
        self.district_id = district_id
        self.user_id = user_id
        self.role_id = role_id
        self.update_date=update_date
        self.recorder_id=recorder_id

    def __repr__(self):
        return '<UserDistrictRole %r>' % (str(self.id))
