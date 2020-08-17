from .. import db

class PPEInventoryView(db.Model):
    __tablename__ = 'ppe_inventory_demand_vw'
    ppe_item_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    facility_id = db.Column(db.String, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    demand7 = db.Column(db.Integer, nullable=False)
    demand14 = db.Column(db.Integer, nullable=False)

    def __init__(self, ppe_item_id, description=None, facility_id=None, quantity=0, demand7=0, demand14=0):
        self.ppe_item_id = ppe_item_id
        self.description = description
        self.facility_id = facility_id
        self.quantity = quantity
        self.demand7 = demand7
        self.demand14 = demand14

    def __repr__(self):
        return '<PPEInventoryView %r>' % (self.description +'@'+self.facility_id)
