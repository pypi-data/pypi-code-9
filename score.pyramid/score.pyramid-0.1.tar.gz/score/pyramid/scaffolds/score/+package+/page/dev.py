from datetime import datetime
import os
from pyramid.renderers import render
from pyramid.view import view_config
import sys
from sqlalchemy import Column, Integer
import traceback
import transaction

import logging
log = logging.getLogger(__name__)


@view_config(route_name='dev/checklist')
def checklist(request):
    here = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(here, 'dev.html')
    request.response.body = open(file, 'rb').read()
    return request.response


def exc2json(excinfo):
    return (
        excinfo[0].__name__,
        str(excinfo[1]),
        traceback.extract_tb(excinfo[2]),
    )


@view_config(route_name='dev/checklist/ajax')
def ajax(request):
    transaction.get().doom()
    try:
        func = {
            'tpl-render': test_tpl_render,
            'css-render': test_css_render,
            'scss-render': test_scss_render,
            'js-render': test_js_render,
            'js-minify': test_js_minify,
            'db-connect': test_db_connect,
            'db-query': test_db_query,
            'db-alter': test_db_alter,
        }[request.matchdict['command']]
        result = func(request)
    except:
        result = exc2json(sys.exc_info())
    request.response.content_encoding = 'UTF-8'
    request.response.content_type = 'application/json; charset=UTF-8'
    request.response.json = result
    return request.response


def test_tpl_render(request):
    assert render('dev/rendertest.jinja2', {}, request) != ''


def test_css_render(request):
    render('reset.css', {}, request)


def test_scss_render(request):
    render('page.scss', {}, request)


def test_js_render(request):
    render('test.js', {}, request)


def test_js_minify(request):
    from score.js.minifier import minify_string
    js = render('test.js', {}, request)
    minify_string(js)


def test_db_connect(request):
    request.db.execute('SELECT 1')


def test_db_query(request):
    with request.db.mktmp([Column('id', Integer)]) as tmp:
        with transaction.manager:
            request.db.execute(tmp.insert().values({'id': 1}))


def test_db_alter(request):
    tbl = 't%d' % datetime.now().timestamp()
    try:
        request.db.execute('CREATE TABLE %s (id INT)' % tbl)
    finally:
        try:
            request.db.execute('DROP TABLE %s' % tbl)
        except:
            pass
