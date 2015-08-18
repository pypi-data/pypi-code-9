# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from hipster_api.management.helpers import search_api
from hipster_api.management.helpers import get_dict
from hipster_api.management.helpers import create_html


class Command(BaseCommand):
    help = u'Зборка api для проекта'

    def handle(self, *args, **kwargs):
        list(map(create_html.render_doc,
                 list(filter(lambda x: x is not None, map(get_dict.format_method_urls, search_api.search_ulrs())))))
