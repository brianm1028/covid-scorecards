from .. import db

class StaffRole(db.Model):
    __tablename__ = 'staff_roles'
    role_type_id = db.Column(db.Integer, primary_key=True)
    role_type = db.Column(db.String)


    def __init__(self, role_type_id, role_type):
        self.role_type_id = role_type_id
        self.role_type = role_type

    def __repr__(self):
        return '<StaffRole %r>' % (self.role_type)
