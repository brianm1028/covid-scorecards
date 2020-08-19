from .. import db
from datetime import datetime

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_types.id'))
    facility_id = db.Column(db.String, db.ForeignKey('facilities.id'))
    room_number = db.Column(db.String)
    capacity = db.Column(db.Integer)
    update_date = db.Column(db.DateTime)
    recorder_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, room_type_id, facility_id, room_number, capacity, recorder_id, update_date=datetime.now()):
        #self.id = id
        self.room_type_id = room_type_id
        self.facility_id = facility_id
        self.room_number = room_number
        self.capacity = capacity
        self.update_date = update_date
        self.recorder_id = recorder_id

    def __repr__(self):
        return '<Room %r>' % (self.room_number + '@' + self.facility_id)
