from .. import db

class RoomType(db.Model):
    __tablename__ = 'room_types'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

    def __init__(self, description):
        #self.id = id
        self.description = description

    def __repr__(self):
        return '<RoomType %r>' % (self.description)
