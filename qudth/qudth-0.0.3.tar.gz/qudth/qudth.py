from functools import partial
import statistics

from sparkprob import sparkprob

from . import sample, aggregate

def qudth(fp, n = None, func = aggregate.length, bins = 20):
    if n:
        get_sample = partial(sample.srs, n)
    else:
        get_sample = sample.census
    X = list(map(func, get_sample(fp)))
    return {
        'min': min(X),
        'max': max(X),
        'mean': statistics.mean(X),
        'median': statistics.median(X),
        'histogram': aggregate.histogram(bins, X),
    }

