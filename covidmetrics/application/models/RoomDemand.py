from .. import db
from datetime import datetime

class RoomDemand(db.Model):
    __tablename__ = 'room_demand'
    id = db.Column(db.Integer, primary_key=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_types.id'))
    facility_id = db.Column(db.String, db.ForeignKey('facilities.id'))
    demand = db.Column(db.Integer)
    update_date = db.Column(db.DateTime)
    recorder_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, room_type_id, facility_id, demand, recorder_id, update_date=datetime.now()):
        #self.id = id
        self.room_type_id = room_type_id
        self.facility_id = facility_id
        self.demand = demand
        self.update_date = update_date
        self.recorder_id = recorder_id

    def __repr__(self):
        return '<RoomDemand %r>' % (str(self.id) + '@' + str(self.update_date))
