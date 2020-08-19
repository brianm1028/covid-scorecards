from .. import db
from datetime import datetime

class PPEInventoryView(db.Model):
    __tablename__ = 'ppe_inventory_vw'
    ppe_item_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    facility_id = db.Column(db.String, primary_key=True)
    facility_name = db.Column(db.String)
    quantity = db.Column(db.Integer, nullable=False)
    update_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, ppe_item_id, description=None, facility_id=None, facility_name=None, quantity=0, update_date=datetime.now()):
        self.ppe_item_id = ppe_item_id
        self.description = description
        self.facility_id = facility_id
        self.facility_name = facility_name
        self.quantity = quantity
        self.update_date = update_date

    def __repr__(self):
        return '<PPEInventoryView %r>' % (self.description +'@'+self.facility_name)
