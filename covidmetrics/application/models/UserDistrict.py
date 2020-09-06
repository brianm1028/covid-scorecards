from .. import db

class UserDistrict(db.Model):
    __tablename__ = 'users_districts'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    district_id = db.Column(db.String, db.ForeignKey('districts.id'), primary_key=True)

    def __init__(self, user_id, district_id):
        self.user_id=user_id
        self.district_id=district_id

    def __repr__(self):
        return '<UserDistrict %r>' % (str(self.user_id) +'-'+self.district_id)
