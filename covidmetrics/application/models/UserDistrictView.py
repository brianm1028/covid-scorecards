from .. import db

class UserDistrictView(db.Model):
    __tablename__ = 'users_districts_vw'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    user_name = db.Column(db.String)
    district_id = db.Column(db.String, db.ForeignKey('districts.id'), primary_key=True)
    district_name = db.Column(db.String)

    def __init__(self, user_id, district_id, user_name, district_name):
        self.user_id=user_id
        self.user_name = user_name
        self.district_id=district_id
        self.district_name = district_name

    def __repr__(self):
        return '<UserDistrictView %r>' % (self.user_name +'-'+self.district_name)
