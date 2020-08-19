from .. import db

class SpaceStatusView(db.Model):
    __tablename__ = 'space_status_vw'
    room_type_id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.String, primary_key=True)
    facility_name = db.Column(db.String)
    description = db.Column(db.String)
    required = db.Column(db.Integer)
    available = db.Column(db.Integer)

    def __init__(self, room_type_id, facility_id, facility_name, description, required, available):
        self.room_type_id = room_type_id
        self.facility_id = facility_id
        self.facility_name = facility_name
        self.description = description
        self.required = required
        self.available = available

    def __repr__(self):
        return '<SpaceStatusView %r>' % (self.description +'@'+self.facility_name)
