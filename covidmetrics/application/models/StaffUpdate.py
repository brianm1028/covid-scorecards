from .. import db

class StaffUpdate(db.Model):
    __tablename__ = 'staff_updates'
    id = db.Column(db.Integer, primary_key=True)
    update_date = db.Column(db.DateTime)
    staff_role_id = db.Column(db.Integer, db.ForeignKey('staff_roles.id'))
    facility_id = db.Column(db.String, db.ForeignKey('facilities.id'))
    recorder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    required = db.Column(db.Integer)
    available = db.Column(db.Integer)


    def __init__(self, id, update_date, staff_role_id, facility_id, required, available, recorder_id):
        self.id = id
        self.update_date = update_date
        self.staff_role_id = staff_role_id
        self.facility_id = facility_id
        self.required = required
        self.available = available
        self.recorder_id = recorder_id

    def __repr__(self):
        return '<StaffUpdate %r>' % (self.id +'@'+self.update_date)
