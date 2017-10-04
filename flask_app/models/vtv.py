from flask_app import db
from datetime import datetime


class VTV(db.Model):
    __tablename__ = 'vtvs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=True)
    yt_id = db.Column(db.String(20), nullable=True, default='')
    yt_status = db.Column(db.String(20), nullable=True, default=0)
    link = db.Column(db.String(255), unique=True)
    category = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    link_mp4 = db.Column(db.Text, nullable=True)
    ins = db.Column(db.Integer, default=datetime.utcnow().strftime('%Y%m%d'))
    source = db.Column(db.String(20), nullable=True, default='vtv')
    tags = db.Column(db.Text, nullable=True)
    # created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title, link, category, description, link_mp4, tags):
        self.title = title
        self.link = link
        self.category = category
        self.description = description
        self.link_mp4 = link_mp4
        self.tags = tags
