from .. import db
import json

class Configuration(db.Model):
    __tablename__ = 'configurations'
    district_id = db.Column(db.String, primary_key=True)
    configuration = db.Column(db.JSON)
    update_date = db.Column(db.DateTime)
    recorder_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def __init__(self, district_id, configuration, update_date, recorder_id):
        self.district_id = district_id
        self.configuration = configuration
        self.update_date = update_date
        self.recorder_id = recorder_id

    def __repr__(self):
        return '<Configuration %r>' % (self.district_id)

    def config(self):
        return self.configuration