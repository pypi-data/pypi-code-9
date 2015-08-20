__author__ = "Johann Klähn <kljohann@gmail.com>"

import collections
import math
import itertools
import datetime

from beancount.core import data
from beancount.core.interpolate import balance_incomplete_postings

__plugins__ = ('split_transactions', )

SplitTransactionsError = collections.namedtuple('SplitTransactionsError', 'source message entry')

def partition(pred, iterable):
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = itertools.tee(iterable)
    return itertools.filterfalse(pred, t1), filter(pred, t2)

def split_transactions(entries, options_map, config=None):
    errors = []
    date_tag = config or 'date'
    has_date_tag = lambda posting: posting.meta and date_tag in posting.meta

    for entry in entries:
        if not isinstance(entry, data.Transaction):
            continue

        references, chunks = map(list, partition(has_date_tag, entry.postings))

        if not chunks:
            continue

        if len(references) != 1:
            errors.append(SplitTransactionsError(
                entry.meta,
                'More than one reference posting (without date tag)',
                entry
            ))
            continue

        if not all(isinstance(posting.meta[date_tag], datetime.date) for posting in chunks):
            errors.append(SplitTransactionsError(
                entry.meta,
                'Posting has malformed date tag',
                entry
            ))
            continue

        for posting in chunks:
            meta = posting.meta.copy()
            date = meta.pop(date_tag)
            new = entry._replace(date=date, postings=[])
            new.postings.append(posting._replace(entry=new, meta=meta))
            # FIXME: Do we want to keep price/position?
            new.postings.append(references[0]._replace(
                entry=new, position=None, price=None))
            balance_incomplete_postings(new, options_map)
            entries.append(new)

        entries.remove(entry)

    return entries, errors