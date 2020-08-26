from .. import db

class PPETransactionsView(db.Model):
    __tablename__ = 'ppe_transactions_vw'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    facility_id = db.Column(db.String, db.ForeignKey("facilities.id"))
    facility_name = db.Column(db.String)
    ppe_item_id = db.Column(db.Integer, db.ForeignKey("ppe_items.id"))
    item_description = db.Column(db.String)
    quantity = db.Column(db.Integer)
    recorder_name = db.Column(db.String)

    def __init__(self, id, date, facility_id, facility_name, ppe_item_id, item_description, quantity, recorder_name):
        self.id = id
        self.date = date
        self.facility_id = facility_id
        self.facility_name = facility_name
        self.ppe_item_id = ppe_item_id
        self.item_description = item_description
        self.quantity = quantity
        self.recorder_name = recorder_name

    def __repr__(self):
        return '<PPETransactionView %r>' % (self.id +'@'+self.date)
