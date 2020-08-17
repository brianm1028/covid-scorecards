from .. import db

class District(db.Model):
    __tablename__ = 'districts'
    id = db.Column(db.String, primary_key=True)
    county_name = db.Column(db.String, db.ForeignKey("counties.name"))
    region_code = db.Column(db.String)
    county_code = db.Column(db.String)
    district_code = db.Column(db.String)
    extra_code = db.Column(db.String)
    district_type = db.Column(db.Integer)
    name = db.Column(db.String)
    base_zip_code = db.Column(db.Integer, db.ForeignKey("zip_codes.zip_code"))
    enabled = db.Column(db.Boolean)


    def __init__(self, id, county_name, region_code, county_code, district_code, extra_code, district_type,
                 name, base_zip_code, enabled):
        self.id = id
        self.county_name = county_name
        self.region_code = region_code
        self.county_code = county_code
        self.district_code = district_code
        self.extra_code = extra_code
        self.district_type = district_type
        self.name = name
        self.base_zip_code = base_zip_code
        self.enabled = enabled

    def __repr__(self):
        return '<District %r>' % (self.district_code + '@' + self.name)
