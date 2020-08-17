from .. import db

class DistrictView(db.Model):
    __tablename__ = 'districts_vw'
    id = db.Column(db.String, primary_key=True)
    district_code = db.Column(db.String)
    name = db.Column(db.String)


    def __init__(self, id, district_code, name):
        self.id = id
        self.district_code = district_code
        self.name = name

    def __repr__(self):
        return '<District %r>' % (self.district_code + '@' + self.name)
