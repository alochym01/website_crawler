from flask import Blueprint, render_template, request, redirect, current_app
from flask_paginate import Pagination, get_page_args

from flask_app import db
from flask_app.models.vtv import VTV

vtvs = Blueprint('vtvs', __name__)


@vtvs.route('/', defaults={'page': 1})
@vtvs.route('/<int:page>')
def index(page):
    print(current_app.config)
    total = VTV.query.count()
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    sql = 'select * from vtvs where yt_status = 0 order by id desc limit {}, {}'.format(
        offset, per_page)
    vtvs = db.engine.execute(sql)
    pagination = Pagination(css_framework='bootstrap4', page=page, alignment='center',
                            per_page=per_page, record_name='vtvs', total=total)
    return render_template('vtv/index.html', vtvs=vtvs, per_page=per_page,
                           page=page, pagination=pagination)


@vtvs.route('/vtvs/test', methods=['POST'])
def vtvs_test():
    missing = VTV.query.filter_by(link=request.get_json().get('link')).first()
    if missing is None:
        return '1'
    return '0'


@vtvs.route('/vtvs/create', methods=['POST'])
def vtvs_create():
    vtv = VTV(
        title=request.get_json().get('title'),
        link=request.get_json().get('link'),
        category=request.get_json().get('category'),
        description=request.get_json().get('description'),
        link_mp4=request.get_json().get('link_mp4'),
        tags=request.get_json().get('tags')
    )
    db.session.add(vtv)
    db.session.commit()
    return 'DONE'


@vtvs.route('/vtvs/update/<int:id>', methods=['GET'])
def vtvs_update(id):
    vtv = VTV.query.filter_by(id=id).first()
    vtv.yt_status = 1
    db.session.add(vtv)
    db.session.commit()
    return redirect(request.referrer)


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap4')
