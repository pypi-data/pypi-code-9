# -*- coding: utf-8 -*-
"""
    statico.helpers
    ---------------
    Defines helper functions
    :license: MIT, see LICENSE for more details.
"""
import os
from pathlib import Path
import datetime
import pytz
from .contents import Page, Article, FileManager
from .generators import Generator
from .utils import parse_metadata
from .readers import Reader
from jinja2.exceptions import TemplateNotFound


def process_files(page_files, article_files, recent_articles, templates_env):
    """
    Process files (pages and articles)

    :param page_files:      list(Path)
    :param article_files:   list(Path)
    :param recent_articles: list
    :param templates_env:   jinja2.environments.Environment
    :return:
    """
    errors = []
    settings = FileManager.get_settings()

    for f in page_files:
        g = Generator(Page.from_file(f), templates_env)
        result = g.generate(recent_articles, settings)

        if not result['status']:
            errors.append(f.name + ' -> ' + result['message'])

    for f in article_files:
        g = Generator(Article.from_file(f), templates_env)
        result = g.generate(recent_articles, settings)

        if not result['status']:
            errors.append(f.name + ' -> ' + result['message'])

    return errors


def process_index(articles, recent_articles, repos, settings, templates_env):
    """
    Process the index file

    :param articles:        list
    :param recent_articles: list
    :param repos:           list
    :param settings:        dict
    :param templates_env:   jinja2.environments.Environment
    :return:
    """
    path = Path(os.path.join('content', 'index.md'))
    fp = path.open()
    rest, data = parse_metadata(fp)
    reader = Reader(rest, 'markdown')
    html = reader.read()

    data['articles'] = articles
    data['content'] = html
    data['paginate'] = data.get('paginate', '').lower() == 'true'
    data['comments'] = False
    if repos:
        data['gh_repos'] = repos
    data['site'] = settings
    data['site']['recent_articles'] = recent_articles

    # Write index.html with default template
    try:
        template = templates_env.get_template('default.html')
    except TemplateNotFound:
        return 'Template not found'
    else:
        page = template.render(data)

    try:
        file_out = open(os.path.join('output', 'index.html'), 'w')
        file_out.write(page)
    except IOError as err:
        file_out.close()
        return 'I/O Error: ' + format(err.errno, err.strerror)
    else:
        file_out.close()

    return None


def process_atom_xml(articles, settings, root_env):
    """
    Process the atom.xml file

    :param articles:
    :param settings:
    :param root_env:
    :return:
    """
    # Fill data
    data = dict(
        articles=articles,
        site=settings
    )
    data['site']['updated'] = datetime.datetime.now(pytz.utc).isoformat()

    # Get template
    try:
        template = root_env.get_template('atom.xml')
    except TemplateNotFound:
        return 'Template not found'
    else:
        atom_xml = template.render(data)

    # Write output file
    try:
        file_out = open(os.path.join('output', 'atom.xml'), 'w')
        file_out.write(atom_xml)
    except IOError as err:
        file_out.close()
        return 'I/O Error: ' + format(err.errno, err.strerror)
    else:
        file_out.close()

    return None
