from itertools import repeat

def length(line):
    start, end = line
    return end - start

def histogram(bins, X):
    _min = min(X)
    _bucketsize = (max(X) - _min) / float(bins)
    if _bucketsize > 0:
        buckets = list(repeat(0, bins))
        for x in X:
            key = int((x - _min) / _bucketsize)
            if key != _min:
                key -= 1
            buckets[key] += 1
        return buckets
