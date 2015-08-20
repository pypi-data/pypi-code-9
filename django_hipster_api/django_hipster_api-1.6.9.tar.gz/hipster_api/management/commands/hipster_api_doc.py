# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from hipster_api.management.helpers import search_api
from hipster_api.management.helpers import get_dict
from hipster_api.management.helpers import create_html


class Command(BaseCommand):
    help = 'Зборка api для проекта'

    def handle(self, *args, **kwargs):
        api = search_api.search_ulrs()
        list(map(create_html.render_doc,
                 list(filter(lambda x: x is not None, map(get_dict.format_method_urls, api)))))
        if all(api):
            self.stdout.write('Список урлов:')

        list(map(lambda x: self.stdout.write('\t - %s %s' % x), api))
