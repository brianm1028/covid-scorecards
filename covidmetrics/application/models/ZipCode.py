from .. import db

class ZipCode(db.Model):
    __tablename__ = 'zip_codes'
    zip_code = db.Column(db.Integer, primary_key=True)
    population = db.Column(db.Integer)
    lat = db.Column(db.Numeric)
    lon = db.Column(db.Numeric)
    county_name = db.Column(db.String)
    city_name = db.Column(db.String)


    def __init__(self, zip_code, population, lat, lon, county_name, city_name):
        self.zip_code = zip_code
        self.population = population
        self.lat = lat
        self.lon = lon
        self.county_name = county_name
        self.city_name = city_name

    def __repr__(self):
        return '<ZipCode %r>' % (str(self.zip_code))
