from .. import db

class StaffUpdate(db.Model):
    __tablename__ = 'staff_updates'
    id = db.Column(db.Integer, primary_key=True)
    update_date = db.Column(db.DateTime)
    staff_role_id = db.Column(db.Integer, db.ForeignKey('staff_roles.id'))
    facility_name = db.Column(db.String, db.ForeignKey('facilities.name'))
    recorder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    required = db.Column(db.Integer)
    available = db.Column(db.Integer)
    #staff_roles = db.relationship("StaffRole", backref=db.backref("staff_roles", uselist=False))
    #facilities = db.relationship("Facility", backref=db.backref("facilities", uselist=False))
    #recorders = db.relationship("User", backref=db.backref("users", uselist=False))


    def __init__(self, id, update_date, staff_role_id, facility_name, required, available, recorder_id):
        self.id = id
        self.update_date = update_date
        self.staff_role_id = staff_role_id
        self.facility_name = facility_name
        self.required = required
        self.available = available
        self.recorder_id = recorder_id

    def __repr__(self):
        return '<StaffUpdate %r>' % (self.id +'@'+self.update_date)
