from flask_app import db


class PACKTPUB(db.Model):
    # query_class = ArticleQuery
    __tablename__ = "packtpubs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    isbn = db.Column(db.String(50), index=True, unique=True)
    # search_vector = db.Column(TSVectorType('title', 'isbn'))

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn

    def __repr__(self):
        return '<PacktPub Title %r>' % (self.title)


# flask_whooshalchemy.whoosh_index(app, PACKTPUB)
