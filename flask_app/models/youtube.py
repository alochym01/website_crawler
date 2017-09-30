from flask_app import db


class YOUTUBE(db.Model):
    __tablename__ = "youtubes"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255))
    published = db.Column(db.String(255))
    status = db.Column(db.String(500), default=1, nullable=True)
    description = db.Column(db.Text())
    title = db.Column(db.String(500))
    yt_videoid = db.Column(db.String(50), index=True, unique=True)

    def __init__(self, author, published, description, title, yt_videoid):
        self.author = author
        self.published = published
        self.description = description
        self.title = title
        self.yt_videoid = yt_videoid

    def __repr__(self):
        return '<Youtube Title %r>' % (self.title)
