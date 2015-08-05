# -*- coding: utf-8 -*-
"""Blueprint sections to import polls from a CSV export."""
from collections import namedtuple
from collective.polls.config import VOTE_ANNO_KEY
from collective.polls.content.poll import IPoll
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from collective.transmogrifier.utils import traverse
from operator import itemgetter
from plone.i18n.normalizer.interfaces import IIDNormalizer
from transmogrify.wppolls.logger import logger
from zope.component import getUtility
from zope.interface import classProvides
from zope.interface import implements

import csv
import os.path

csv_options = dict(dialect='excel-tab', doublequote=False, escapechar='\\')


class CSVSource(object):

    """Blueprint section to import polls from a CSV export."""

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.source = options.get('source')
        self.type = 'collective.polls.poll'
        # default path where the polls are going to be imported
        self.path = options.get('path', '/polls')
        # transitions is a list of transition names
        self.transitions = options.get(
            'transitions', 'open, close').replace(' ', '').split(',')
        self.locale = options.get('path', 'en')
        self.results = self._get_results
        self.normalizer = getUtility(IIDNormalizer)

    def __iter__(self):
        for item in self.previous:
            yield item

        filename = os.path.join(self.source, 'wp_pollsq.csv')
        assert os.path.isfile(filename), 'Missing file: ' + filename

        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile, **csv_options)
            for row in reader:

                item = dict()
                # quotes on title are escaped
                item['title'] = row['pollq_question'].replace('\\"', '"')
                item_id = unicode(item['title'], 'utf-8')
                item_id = self.normalizer.normalize(item_id, locale=self.locale)

                timestamp = int(row['pollq_timestamp'])
                # DateTime accepts timestamps also
                item['creation_date'] = timestamp
                item['effective_date'] = timestamp
                item['modification_date'] = timestamp

                poll_id = row['pollq_id']
                item['_results'] = self.results[poll_id]

                item['_type'] = self.type
                item['_path'] = '/'.join([self.path, item_id])
                item['_transitions'] = tuple(self.transitions)

                yield item

    @property
    def _get_results(self):
        """Return a mapping between a poll and its results.

        :returns: the results of each poll
        :rtype: list of dictionaries
        """
        logger.info('Parsing "wp_pollsa.csv" file')
        filename = os.path.join(self.source, 'wp_pollsa.csv')
        assert os.path.isfile(filename), 'Missing file: ' + filename

        Result = namedtuple('Result', ['id', 'answer', 'votes'])
        mapping = dict()
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile, **csv_options)
            for row in reader:
                aid = row['polla_aid']
                qid = row['polla_qid']
                answer = row['polla_answers']
                votes = row['polla_votes']
                mapping.setdefault(qid, []).append(
                    Result(aid, answer, int(votes)))

        for i in mapping.keys():
            # sort answers by aid
            mapping[i] = sorted(mapping[i], key=itemgetter(0))

        return mapping


class VoteUpdater(object):

    """Blueprint section to update votes on a poll."""

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

    def __iter__(self):
        for item in self.previous:

            pathkey = self.pathkey(*item.keys())[0]
            if not pathkey:  # not enough info
                yield item
                continue
            path = item[pathkey]

            obj = traverse(self.context, str(path).lstrip('/'), None)
            if obj is None:  # object not found
                yield item
                continue

            if not IPoll.providedBy(obj):  # not a poll
                yield item
                continue

            if '_results' not in item:  # no results
                yield item
                continue

            # item['_results'] contains a list of named tuples:
            # namedtuple('Result', ['id', 'answer', 'votes'])
            obj.options = []
            for o, option in enumerate(item['_results']):
                obj.options.append(
                    dict(option_id=o, description=option.answer))
                key = VOTE_ANNO_KEY % o
                obj.annotations[key] = option.votes

            yield item
