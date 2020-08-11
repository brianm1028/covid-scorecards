from .. import db

class StaffRole(db.Model):
    __tablename__ = 'staff_roles'
    id = db.Column(db.Integer, primary_key=True)
    role_type = db.Column(db.String)


    def __init__(self, id, role_type):
        self.id = id
        self.role_type = role_type

    def __repr__(self):
        return '<StaffRole %r>' % (self.role_type)
