from .. import db

class COVIDRegion(db.Model):
    __tablename__ = 'covid_regions'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    population = db.Column(db.Integer)


    def __init__(self, id, description, population):
        self.id = id
        self.description = description
        self.population = population

    def __repr__(self):
        return '<COVIDRegion %r>' % (str(self.id) + '@' + self.description)
