from .. import db

class RoomDemand(db.Model):
    __tablename__ = 'room_demand'
    id = db.Column(db.Integer, primary_key=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_types.id'))
    facility_name = db.Column(db.String, db.ForeignKey('facilities.name'))
    demand = db.Column(db.Integer)
    update_date = db.Column(db.DateTime)
    recorder_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, id, room_type_id, facility_name, demand, update_date, recorder_id):
        self.id = id
        self.room_type_id = room_type_id
        self.facility_name = facility_name
        self.demand = demand
        self.update_date = update_date
        self.recorder_id = recorder_id

    def __repr__(self):
        return '<RoomDemand %r>' % (self.id + '@' + self.update_date)
