from __future__ import absolute_import

import redisext.models.abc


class Pool(redisext.models.abc.Model):
    def pop(self):
        '''
        Pop item from pool.

        :returns: obviously item
        :rtype: how knows(serializer knows)
        '''
        item = self.connect_to_master().spop(self.key)
        return self.decode(item)

    def push(self, item):
        '''
        Place item into pool.

        :param item: whatever you need to place into pool
        :rtype: bool
        '''
        item = self.encode(item)
        return bool(self.connect_to_master().sadd(self.key, item))


class SortedSet(redisext.models.abc.Model):
    def add(self, element, score):
        element = self.encode(element)
        return bool(self.connect_to_master().zadd(self.key, score, element))

    def rem(self, element):
        element = self.encode(element)
        return bool(self.connect_to_master().zrem(self.key, element))

    def length(self, start_score, end_score):
        return int(self.connect_to_slave().zcount(self.key, start_score, end_score))

    def members(self, with_scores=False):
        elements = self.connect_to_slave().zrevrange(self.key, 0, -1, withscores=with_scores)
        if not elements:
            return elements

        if with_scores:
            return [(s, self.decode(e)) for e, s in elements]
        else:
            return [self.decode(e) for e in elements]

    def members_by_score(self, min_score='-inf', max_score='+inf', with_scores=False):
        elements = self.connect_to_slave().zrangebyscore(self.key, min_score, max_score, num=-1, withscores=with_scores)
        if not elements:
            return elements

        if with_scores:
            return [(s, self.decode(e)) for e, s in elements]
        else:
            return [self.decode(e) for e in elements]

    def contains(self, element):
        element = self.encode(element)
        return self.connect_to_slave().zscore(self.key, element) is not None

    def truncate(self, size):
        return int(self.connect_to_master().zremrangebyrank(self.key, 0, -1 * size - 1))

    def clean(self):
        return bool(self.connect_to_master().delete(self.key))

    def clean_by_score(self, min_score, max_score):
        elements = self.connect_to_master().zremrangebyscore(self.key, min_score, max_score)
        return bool(elements)
