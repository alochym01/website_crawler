from flask_app import db


class PACKTPUB(db.Model):
    __tablename__ = "packtpubs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    isbn = db.Column(db.String(50), index=True, unique=True)

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn

    def __repr__(self):
        return '<PacktPub Title %r>' % (self.title)
