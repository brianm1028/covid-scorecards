from .. import db

class PPEItem(db.Model):
    __tablename__ = 'ppe_items'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

    def __init__(self, id, description):
        self.id = id
        self.description = description

    def __repr__(self):
        return '<PPEItem %r>' % (self.description)
