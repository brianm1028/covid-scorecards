from .. import db

class Facility(db.Model):
    __tablename__ = 'facilities'
    id = db.Column(db.String, primary_key=True)
    district_id = db.Column(db.String, db.ForeignKey("districts.id"))
    facility_name = db.Column(db.String)
    zip_code = db.Column(db.Integer, db.ForeignKey("zip_codes.zip_code"))
    grades_served = db.Column(db.String)

    def __init__(self, id, district_id, facility_name, zip_code, grades_served):
        self.id = id
        self.district_id = district_id
        self.facility_name = facility_name
        self.zip_code = zip_code
        self.grades_served = grades_served

    def __repr__(self):
        return '<Facility %r>' % (self.facility_name)
