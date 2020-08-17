from .. import db

class StaffStatusView(db.Model):
    __tablename__ = 'staff_status_vw'
    update_date = db.Column(db.DateTime)
    role_type = db.Column(db.String, primary_key=True)
    facility_id = db.Column(db.String, primary_key=True)
    required = db.Column(db.Integer)
    available = db.Column(db.Integer)
    recorder_name = db.Column(db.String)

    def __init__(self, update_date, role_type, facility_id, required, available, recorder_name):
        self.update_date = update_date
        self.role_type = role_type
        self.facility_id = facility_id
        self.required = required
        self.available = available
        self.recorder_name = recorder_name

    def __repr__(self):
        return '<StaffStatusView %r>' % (self.role_type +'@'+self.facility_id)
