from flask_wtf import FlaskForm
from wtforms import TextField, StringField
from wtforms.validators import DataRequired, EqualTo, Length


class YoutubeForm(FlaskForm):
    author = StringField('author', validators=[DataRequired()])
    published = StringField('published', validators=[DataRequired()])
    status = StringField('status', validators=[DataRequired()])
    description = TextField('description', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    yt_videoid = StringField('yt_videoid', validators=[DataRequired()])
