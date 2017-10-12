import json
import os
import re
import shlex
from random import randint
from subprocess import PIPE, Popen

from flask import Blueprint, redirect, render_template, request, url_for
from flask_paginate import Pagination, get_page_args
from pytube import YouTube

from flask_app import celery_app, db
from flask_app.forms import YoutubeForm
from flask_app.models.youtube import YOUTUBE

TOP_LEVEL_DIR = os.path.abspath(os.curdir)


youtube = Blueprint('youtube', __name__)


@youtube.route('/video', defaults={'page': 1})
@youtube.route('/video/<int:page>')
def index(page):
    total = YOUTUBE.query.count()
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    sql = 'select * from youtubes order by id desc limit {}, {}'.format(
        offset, per_page)
    print(sql)
    youtubes = db.engine.execute(sql)
    pagination = Pagination(css_framework='bootstrap4', page=page, total=total,
                            alignment='center', per_page=per_page, record_name='youtube')
    return render_template('youtube/index.html', youtubes=youtubes, page=page, per_page=per_page, pagination=pagination)


@youtube.route('/video/create', methods=['POST'])
def youtube_create():
    youtube = YOUTUBE(
        author=request.get_json().get('author'),
        published=request.get_json().get('published'),
        description=request.get_json().get('description'),
        title=request.get_json().get('title'),
        yt_videoid=request.get_json().get('yt_videoid')
    )
    db.session.add(youtube)
    db.session.commit()
    msg = {
        "id": youtube.id,
        'title': youtube.title,
        'yt_videoid': youtube.yt_videoid
    }
    upload_youtube.delay(msg)
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


@celery_app.task()
def upload_youtube(msg):
    """Background task to download and upload video to youtube"""
    url = "https://www.youtube.com/watch?v=%s" % msg['yt_videoid']
    fname = "%s/download_file/%s.mp4" % (TOP_LEVEL_DIR, randint(1, 1000000000))
    cmd = "/home/hadn/py4code/bin/youtube-dl -o %s %s" % (fname, url)
    cmd = shlex.split(cmd)
    up = Popen(cmd, stdout=PIPE)
    temp = up.communicate()

    cmd_upload = "/home/hadn/py4code/bin/python %s/flask_app/crawler/upload_youtube.py --file %s --title '%s'" % (
        TOP_LEVEL_DIR, fname, msg['title'])
    cmd_upload = shlex.split(cmd_upload)
    up_youtube = Popen(cmd_upload, stdout=PIPE)
    temp_upload = up_youtube.communicate()

    print(temp_upload)
    return msg


# def upload_youtube(link, title, desc, keyword):
#     os.chdir('/mnt/website/v1/laravel')
#     wget.download(link)
#     file_mp4 = link.split("/")[-1]
#     cmd = '/home/hadn/python3/bin/python /mnt/website/v1/vtv_crawler/upload_youtube.py --file "%s" --title "%s" --description "%s" --keywords "%s" --category=25' % (
#         file_mp4, title, desc, keyword)
#     cmd = shlex.split(cmd.encode('utf8'))
#     print(cmd)
#     try:
#         up = Popen(cmd, stdout=PIPE)
#         temp = up.communicate()
#         #: remove file which uploaded to youtube
#         os.remove(file_mp4)
#         return temp[0].decode('utf-8').strip().split("'")[1]
#     except Exception as e:
#         print(str(e))
#         pass


# def add_to_playlist(videoId):
#     cmd = '/home/hadn/python3/bin/python /mnt/website/v1/vtv_crawler/playlist_item.py --videoId %s' % (
#         videoId)
#     cmd = shlex.split(cmd.encode('utf8'))
#     print(cmd)
#     try:
#         up = Popen(cmd, stdout=PIPE)
#         temp = up.communicate()
#     except Exception as e:
#         print(str(e))
#         pass
