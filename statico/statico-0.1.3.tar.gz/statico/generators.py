# -*- coding: utf-8 -*-

__version__ = '0.1.3'
__author__ = 'Ossama Edbali (ossedb@gmail.com)'


import os
from .contents import FileManager
from .readers import Reader
from .utils import get_gh_repos, parse_metadata


class Generator(object):
    def __init__(self, item, templates_env):
        self.item = item
        self.templates_env = templates_env
        self.content = None
        self.context = None

    def generate(self, recent_articles):

        settings = FileManager.get_settings()
        self.content, self.context = parse_metadata(self.item.get_file_pointer('r'))
        reader = Reader(self.content, self.item.extension)
        html = reader.read()

        target_dir = self.item.get_output_directory()

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Get template
        try:
            layout = self.context['layout']
        except KeyError:
            return False

        template = self.templates_env.get_template(layout + '.html')

        # Update context
        self.context['content'] = html
        self.context['url'] = self.item.get_url()
        self.context['comments'] = True
        self.context['site'] = settings
        self.context['site']['recent_articles'] = recent_articles

        # Process GH repos
        if settings.get('github_user'):
            self.context['gh_repos'] = get_gh_repos(settings.get('github_user'), settings.get('github_repo_count'))

        # Process categories
        if self.context.get('categories'):
            FileManager.process_categories(self.context, self.templates_env)

        # Write file to output
        page = template.render(self.context)
        file_out = open(os.path.join(target_dir, 'index.html'), 'w')
        file_out.write(page)
        file_out.close()
