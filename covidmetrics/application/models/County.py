from .. import db

class County(db.Model):
    __tablename__ = 'counties'
    name = db.Column(db.String, primary_key=True)
    population = db.Column(db.Integer)
    region = db.Column(db.Integer)
    lat = db.Column(db.Numeric)
    lon = db.Column(db.Numeric)
    COVIDRegion = db.Column(db.Integer, db.ForeignKey('covid_regions.id'))


    def __init__(self, name, population, region, lat, lon, COVIDRegion):
        self.name = name
        self.population = population
        self.region = region
        self.lat = lat
        self.lon = lon
        self.COVIDRegion = COVIDRegion

    def __repr__(self):
        return '<County %r>' % (self.name)
