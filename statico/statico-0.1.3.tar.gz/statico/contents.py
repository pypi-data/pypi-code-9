# -*- coding: utf-8 -*-

__version__ = '0.1.3'
__author__ = 'Ossama Edbali (ossedb@gmail.com)'


import os
import datetime
import json
import shutil
import pytz
from pathlib import Path
from slugify import slugify
from .utils import copy_directory
from .pylog import action
from .utils import parse_metadata
from .readers import Reader


class Page(object):
    def __init__(self, title, author, date=None, extension='md'):
        if date is None:
            date = datetime.date.today().isoformat()

        self.title = title
        self.title_slug = slugify(title)
        self.author = author
        self.date = date
        self.extension = extension
        self.directory = os.path.join('content', 'pages')
        self.layout = 'page'
        self.exclude_meta = ['exclude_meta', 'url', 'title_slug', 'extension', 'directory']

    @classmethod
    def from_file(cls, file_path):
        fp = file_path.open()
        _, context = parse_metadata(fp)
        fp.close()

        return cls(context.get('title'), context.get('author'), context.get('date_iso'), file_path.name.split('.')[1])

    @staticmethod
    def get_url_from(title_slug):
        return '/' + title_slug

    def get_url(self):
        return '/' + self.title_slug

    def get_path(self):
        filename = os.path.join(self.directory, self.title_slug + '.' + self.extension)
        return Path(filename)

    def get_default_metadata(self):
        dm = self.__dict__
        ls = ['---\n']

        for key in sorted(dm):
            if key not in self.exclude_meta:
                value = dm.get(key)

                if isinstance(value, list):
                    value = ', '.join(value)
                ls.append(key + ': ' + value + '\n')

        ls.append('---\n')

        return ls

    def get_file_pointer(self, mode='w'):
        return self.get_path().open(mode)

    def get_output_directory(self):
        return os.path.join('output', self.title_slug)

    def create(self):
        try:
            fp = self.get_file_pointer()
            fp.writelines(self.get_default_metadata())
            fp.close()
        except OSError:
            return False

        return True


class Article(Page):
    def __init__(self, title, author, date=None, extension='md', categories=None):
        super(Article, self).__init__(title, author, date, extension)

        if categories is None:
            categories = []

        self.title_slug = self.date + '-' + slugify(self.title)
        self.categories = categories
        self.directory = os.path.join('content', 'articles')
        self.layout = 'article'

    @staticmethod
    def get_url_from(o):
        if isinstance(o, str):
            dirs = o.split('-', maxsplit=3)
            return 'blog/' + '/'.join(dirs)

        if isinstance(o, list):
            return 'blog/' + '/'.join(o)

        return None

    @staticmethod
    def get_articles(f_articles, content=True):
        articles = []

        for f_article in f_articles:
            fp = f_article.open()
            filename_parts = f_article.name.split('.')

            rest, data = parse_metadata(fp)
            data['url'] = Article.get_url_from(filename_parts[0])
            data['updated'] = datetime.datetime.fromtimestamp(os.path.getmtime(str(f_article)), tz=pytz.utc).isoformat()

            if content:
                reader = Reader(rest, reader_type=filename_parts[1])
                data['content'] = reader.read()

            articles.append(data)
            fp.close()

        return articles

    def get_url(self):
        return 'blog/' + self.title_slug

    def get_output_directory(self):
        paths = ['output', 'blog']
        paths.extend(self.date.split('-'))
        paths.append(slugify(self.title))
        return os.path.join(*paths)


class FileManager(object):
    @staticmethod
    def get_settings():
        return json.load(open('settings.json'))

    @staticmethod
    def process_categories(data, env):
        categories = data.get('categories')
        category_template = env.get_template('category.html')

        if categories:
            articles = []
            data['categories'] = categories.replace(' ', '').split(',')

            # Loop through categories
            for category in data['categories']:
                category_dir = os.path.join('output', 'blog', 'categories', category)
                if os.path.exists(category_dir):
                    continue

                os.makedirs(category_dir)

                # Render page and save category file
                category_page = category_template.render(dict(
                    category=category,
                    site=FileManager.get_settings(),
                    articles=[a for a in articles if category in a.get('categories', '')]  # ===> FIX
                ))
                category_file = open(os.path.join(category_dir, 'index.html'), 'w')
                category_file.write(category_page)
                category_file.close()

    @staticmethod
    def create_project():
        path = os.path.abspath(__file__)
        dir_path = os.path.join(os.path.dirname(path), 'data')

        open('.statico', 'w')

        # Settings
        shutil.copy(os.path.join(dir_path, 'settings.json'), 'settings.json')
        print(action('settings.json'))

        # Atom XML
        shutil.copy(os.path.join(dir_path, 'atom.xml'), 'atom.xml')
        print(action('atom.xml'))

        # Static
        static_path = os.path.join(dir_path, 'static')
        copy_directory(static_path, 'static')
        print(action('Static assets'))

        # Templates
        templates_path = os.path.join(dir_path, 'templates')
        copy_directory(templates_path, 'templates')
        print(action('Templates'))

        # Content
        os.makedirs('content')
        os.makedirs(os.path.join('content', 'articles'))
        os.makedirs(os.path.join('content', 'pages'))
        index = open(os.path.join('content', 'index.md'), 'w')
        index.writelines([
            '---\n',
            'layout: default\n',
            'paginate: true\n',
            '---\n'
        ])
        print(action('Contents directory'))

        # Output
        os.makedirs('output')
        print(action('Output directory'))

    @staticmethod
    def clear_workspace():
        if os.path.isfile('settings.json'):
            os.remove('settings.json')

        if os.path.isfile('atom.xml'):
            os.remove('atom.xml')

        if os.path.isfile('.statico'):
            os.remove('.statico')

        shutil.rmtree('content', True)
        shutil.rmtree('output', True)
        shutil.rmtree('static', True)
        shutil.rmtree('templates', True)
