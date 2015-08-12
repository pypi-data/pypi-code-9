import os

from flask import Flask, render_template

import simpress.page


def create_app():
    app = Flask(__name__,
                static_url_path='',
                static_folder=simpress.base_dir,
                template_folder=os.path.join(simpress.base_dir, '_templates'))
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.debug = True

    app.add_url_rule('/', defaults={'path': 'index'}, view_func=render_page)
    app.add_url_rule('/<path:path>.html', view_func=render_page)

    return app


def find_file(path):
    return os.path.join(simpress.base_dir, '%s.md' % path)


def render_page(path):
    return render_template(
        'page.html',
        settings=simpress.settings,
        root='../' * path.count('/'),
        page=simpress.page.parse_file(find_file(path)))
