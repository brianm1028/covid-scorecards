from .. import db
import json

class Configuration(db.Model):
    __tablename__ = 'configurations'
    district_id = db.Column(db.String, primary_key=True)
    configuration = db.Column(db.JSON)

    def __init__(self, district_id, configuration):
        self.district_id = district_id
        self.configuration = configuration

    def __repr__(self):
        return '<Configuration %r>' % (self.district_id)

    def config(self):
        return self.configuration