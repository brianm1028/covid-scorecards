from .. import db

class PPETransaction(db.Model):
    __tablename__ = 'ppe_transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    ppe_item_id = db.Column(db.Integer, db.ForeignKey('ppe_items.id'))
    facility_id = db.Column(db.String, db.ForeignKey('facilities.id'))
    quantity = db.Column(db.Integer)
    recorder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ppe_item = db.relationship("PPEItem", backref=db.backref("ppe_items", uselist=False))
    facility = db.relationship("Facility", backref=db.backref("facilities", uselist=False))
    recorder = db.relationship("User", backref=db.backref("users", uselist=False))

    def __init__(self, id, date, ppe_item_id, facility_id, quantity, recorder_id):
        self.id = id
        self.ppe_item_id = ppe_item_id
        self.facility_id = facility_id
        self.quantity = quantity
        self.recorder_id = recorder_id

    def __repr__(self):
        return '<PPETransaction %r>' % (self.id +'@'+self.date)
