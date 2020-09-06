from .. import db

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    role_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    permset = db.Column(db.Integer)

    def __init__(self, role_id, description, permset):
        self.role_id=role_id
        self.description=description
        self.permset=permset

    def __repr__(self):
        return '<UserRole %r>' % (self.description)
