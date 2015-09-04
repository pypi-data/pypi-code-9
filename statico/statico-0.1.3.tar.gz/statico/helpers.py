# -*- coding: utf-8 -*-

__version__ = '0.1.3'
__author__ = 'Ossama Edbali (ossedb@gmail.com)'


import os
from pathlib import Path
import datetime
import markdown
import pytz
from .contents import Page, Article
from .generators import Generator
from .utils import parse_metadata


def process_files(page_files, article_files, recent_articles, templates_env):

    for f in page_files:
        g = Generator(Page.from_file(f), templates_env)
        g.generate(recent_articles)

    for f in article_files:
        g = Generator(Article.from_file(f), templates_env)
        g.generate(recent_articles)


def process_index(articles, recent_articles, repos, settings, templates_env):
    path = Path(os.path.join('content', 'index.md'))
    fp = path.open()
    rest, data = parse_metadata(fp)
    html = markdown.markdown('\n'.join(rest), extensions=['markdown.extensions.extra',
                                                          'markdown.extensions.codehilite'])

    data['articles'] = articles
    data['content'] = html
    data['paginate'] = data['paginate'] == 'true'
    data['comments'] = False
    if repos:
        data['gh_repos'] = repos
    data['site'] = settings
    data['site']['recent_articles'] = recent_articles

    # Write index.html with default template
    template = templates_env.get_template('default.html')
    page = template.render(data)
    open(os.path.join('output', 'index.html'), 'w').write(page)


def process_atom_xml(articles, settings, root_env):
    # Fill data
    data = dict(
        articles=articles,
        site=settings
    )
    data['site']['updated'] = datetime.datetime.now(pytz.utc).isoformat()

    template = root_env.get_template('atom.xml')
    atom_xml = template.render(data)
    open(os.path.join('output', 'atom.xml'), 'w').write(atom_xml)