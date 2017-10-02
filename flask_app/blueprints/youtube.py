from flask import Blueprint, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_args

from flask_app import db
from flask_app.models.youtube import YOUTUBE
from flask_app.forms import YoutubeForm

youtube = Blueprint('youtube', __name__)


@youtube.route('/video', defaults={'page': 1})
@youtube.route('/video/<int:page>')
def index(page):
    total = YOUTUBE.query.count()
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    sql = 'select * from youtubes where status = 0 order by id desc limit {}, {}'.format(
        offset, per_page)
    youtubes = db.engine.execute(sql)
    pagination = Pagination(page=page, per_page=per_page, record_name='youtube',
                            total=total)
    return render_template('youtube/index.html', youtube=youtubes, per_page=per_page,
                           page=page, pagination=pagination)


@youtube.route('/video/create', methods=['POST'])
def youtube_create():
    youtube = YOUTUBE(
        author=request.get_json().get('author'),
        published=request.get_json().get('published'),
        description=request.get_json().get('description'),
        title=request.get_json().get('title'),
        yt_videoid=request.get_json().get('yt_videoid')
    )
    try:
        db.session.add(youtube)
        db.session.commit()
    except:
        db.session.rollback()
    return 'DONE'


@youtube.route('/video/edit/<int:id>', methods=['GET', 'POST'])
def youtube_edit(id):
    form = YoutubeForm()
    youtube = YOUTUBE.query.get_or_404(id)

    if form.validate_on_submit():
        youtube.author = form.author.data
        youtube.published = form.published.data
        youtube.description = form.description.data
        youtube.title = form.title.data
        youtube.yt_videoid = form.yt_videoid.data
        youtube.status = form.status.data
        db.session.add(youtube)
        db.session.commit()
        return redirect(url_for('youtube.index'))
    return render_template('youtube/edit.html', form=form, youtube=youtube)
