from .. import db

class Facility(db.Model):
    __tablename__ = 'facilities'
    name = db.Column(db.String, primary_key=True)
    district = db.Column(db.Integer)

    def __init__(self, name, district):
        self.name = name
        self.district = district

    def __repr__(self):
        return '<Facility %r>' % (self.name)
