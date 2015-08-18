# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
import os
import shutil
from django.template.loader import render_to_string
from django.conf import settings as dj_settings


def rm_r(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)

rm_r(os.path.join(dj_settings.TEMPLATE_DIRS[0], 'docs', 'menu2.html'))
rm_r(os.path.join(dj_settings.TEMPLATE_DIRS[0], 'docs', 'files'))
os.mkdir(os.path.join(dj_settings.TEMPLATE_DIRS[0], 'docs', 'files'))


def render_doc(item):
    url = '/docs/api%s' % item['url'].replace('.json', '')
    body = render_to_string('docs/skeleton/body2.html', item)
    file_name = 'docs_api%s' % item['url'].replace('/', '_').replace('.json', '.html')
    file_name = os.path.join(dj_settings.TEMPLATE_DIRS[0], 'docs', 'files', file_name)
    f = io.open(file_name, 'w+', encoding='utf8')
    f.write(body)
    f.close()

    menu_patch = os.path.join(dj_settings.TEMPLATE_DIRS[0], 'docs', 'menu2.html')
    f = io.open(menu_patch, 'a+', encoding='utf8')
    f.write(render_to_string('docs/skeleton/menu2.html', {'url': url, 'name': item['text'], 'class': item['class']}))
    f.close()
