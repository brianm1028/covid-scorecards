from .. import db
from datetime import datetime

class PPETransaction(db.Model):
    __tablename__ = 'ppe_transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    ppe_item_id = db.Column(db.Integer, db.ForeignKey('ppe_items.id'))
    facility_id = db.Column(db.String, db.ForeignKey('facilities.id'))
    quantity = db.Column(db.Integer)
    recorder_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, ppe_item_id, facility_id, quantity, recorder_id, date=datetime.now()):
        #self.id = id
        self.date = date
        self.ppe_item_id = ppe_item_id
        self.facility_id = facility_id
        self.quantity = quantity
        self.recorder_id = recorder_id

    def __repr__(self):
        return '<PPETransaction %r>' % (self.id +'@'+self.date)
