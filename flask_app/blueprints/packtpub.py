from flask import Blueprint, render_template, request, redirect, current_app
from flask_paginate import Pagination, get_page_args

from flask_app import db
from flask_app.models.packtpub import PACKTPUB

packtpubs = Blueprint('packtpubs', __name__)


@packtpubs.route('/packtpubs', defaults={'page': 1})
@packtpubs.route('/pactpubs/<int:page>')
def index(page):
    print(current_app.config)
    total = PACKTPUB.query.count()
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    sql = 'select * from packtpubs order by id desc limit {}, {}'.format(
        offset, per_page)
    packtpubs = db.engine.execute(sql)
    pagination = Pagination(css_framework='bootstrap4', page=page, alignment='center',
                            per_page=per_page, record_name='packtpubs', total=total)
    return render_template('packtpub/index.html', packtpubs=packtpubs, per_page=per_page,
                           page=page, pagination=pagination)


@packtpubs.route('/packtpubs/create', methods=['POST'])
def packtpubs_create():
    packtpub = PACKTPUB(
        title=request.get_json().get('title'),
        isbn=request.get_json().get('isbn')
    )
    db.session.add(packtpub)
    db.session.commit()
    return 'DONE'
