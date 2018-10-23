from .app import db


class Name(db.Model):
    __tablename__ = 'telemarkers_db'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64))

    def __repr__(self):
        return '<Pet %r>' % (self.Name)
