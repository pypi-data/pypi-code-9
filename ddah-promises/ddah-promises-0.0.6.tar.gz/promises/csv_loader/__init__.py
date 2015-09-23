# -*- coding: utf-8 -*-
import re

def match_with(first_part, key):
    pattern = re.compile('_(?P<id>\d+)$')
    return first_part + str(pattern.search(key).group('id'))


HEADER_TYPES = {'id': {'what': 'promise_kwarg', 'as': 'identifier'},
                'category': {'what': 'promise_kwarg'},
                'promess': {'what': 'promise_kwarg', 'as': 'name'},
                'description': {'what': 'promise_kwarg'},
                'quality': {'what': 'promise_kwarg'},
                'fulfillment': {'what': 'promise_kwarg'},
                'ponderator': {'what': 'promise_kwarg'},
                'verification_doc_name_(?P<id>\d+)': {'what': 'verification_doc_kwarg',
                                                      'match': 'verification_doc_link_',
                                                      'use_this_as': 'name',
                                                      'use_other_as': 'url'
                                                      },
                'information_source_name_(?P<id>\d+)': {'what': 'information_source_kwarg',
                                                      'match': 'information_source_link_',
                                                      'use_this_as': 'name',
                                                      'use_other_as': 'url'
                                                      },
                'tag': {'what': 'create_tag_arg'},
}
CREATION_ORDER = [{'name': 'promise',
                   'multiple': False},
                  {'name': 'verification_doc',
                   'multiple': True
                   },
                  {'name': 'information_source',
                   'multiple': True
                   }]

from .creator import *
from .processor import *
from .csv_processor import *
