"""
clients for getting and processing pageview data
"""

import json

import requests

from .models import Trend


class BasePageviewClient(object):
    """an object used to get pageview data from the pageview-* suite
    """

    DEFAULT_SCHEME = "http://"

    def __init__(self, hostname, endpoint, scheme=DEFAULT_SCHEME):
        """initializes a BasePageviewClient

        :param hostname: the hostname portion of the request
        :type hostname: str

        :param endpoint: the reading endpoint portion of the request
        :type endpoint: str

        :param scheme: the http/1.1 scheme of the request - defaults to "http://"
        :type scheme: str
        """
        self.data = {}
        self.url = self._build_url(scheme, hostname, endpoint)

    @classmethod
    def _clean_scheme(cls, scheme):
        if not scheme.endswith("://"):
            scheme += "://"
        return scheme

    @classmethod
    def _clean_hostname(cls, hostname):
        if not hostname.endswith("/"):
            hostname += "/"
        return hostname

    @classmethod
    def _build_url(cls, scheme, hostname, endpoint):
        scheme = cls._clean_scheme(scheme)
        hostname = cls._clean_hostname(hostname)
        return "{}{}{}".format(scheme, hostname, endpoint)

    def get(self, *args, **kwargs):
        raise NotImplementedError


class TrendingClient(BasePageviewClient):
    """a client for getting trending data from the *_trends tables
    """

    DEFAULT_ENDPOINT = "trending.json"

    def __init__(self, hostname, endpoint=DEFAULT_ENDPOINT, scheme=BasePageviewClient.DEFAULT_SCHEME):
        """initializes a TrendingClient

        :param hostname: the hostname portion of the request
        :type hostname: str

        :param endpoint: the reading endpoint portion of the request - defaults to "trending.json"
        :type endpoint: str

        :param scheme: the http/1.1 scheme of the request - defaults to "http://"
        :type scheme: str
        """
        super(TrendingClient, self).__init__(hostname, endpoint, scheme)

    def get(self, site, offset=None, limit=None):
        """gets data from a corresponding trends table and sets `self.data` to a list of `Trend` objects

        :param site: the site name corresponding to the table
        :type site: str

        :param offset: the number of minutes to go back to aggregate
        :type offset: int

        :param limit: the maximum number of results to return
        :type limit: int

        :return: a list of content ids
        :rtype: list
        """
        url = self.url
        url += "?site={}".format(site)
        if offset:
            url += "&offset={}".format(offset)
        if limit:
            url += "&limit={}".format(limit)
        response = requests.get(url)
        if response.ok:
            try:
                parsed_data = json.loads(str(response.content, 'utf-8'))
            except TypeError:
                parsed_data = json.loads(response.content)
            trend_data = sorted(
                [Trend(**obj) for obj in parsed_data],
                key=lambda trend: trend.score,
                reverse=True
            )
            self.data = dict([(t.content_id, t) for t in trend_data])
            return [trend.content_id for trend in trend_data]
        else:
            return []


class DjangoTrendingClient(TrendingClient):
    """a subclass of TrendingClient with convenience wrappers for generating a list of model instances
    """

    def __init__(self, in_bulk_method, fallback_method, *args, **kwargs):
        """initializes a TrendingClient

        :param in_bulk_method: the method call to get the model instances in bulk
        :type in_bulk_method: instancemethod

        :param fallback_method: the method call to get model instances in the event no data is returned from `get`
        :type fallback_method: instancemethod

        :param hostname: the hostname portion of the request
        :type hostname: str

        :param endpoint: the reading endpoint portion of the request - defaults to "trending.json"
        :type endpoint: str

        :param scheme: the http/1.1 scheme of the request - defaults to "http://"
        :type scheme: str

        >>> from pageview_client.clients DjangoTrendingClient
        >>> from django.db import models
        >>> class SomeModel(models.Model):
        ...     pass
        ...
        >>> client = DjangoTrendingClient(
        ...     in_bulk_method=SomeModel.objects.in_bulk,  # later called as self.in_bulk()
        ...     fallback=SomeModel.objects.all,  # later called as self.fallback() when self.data == []
        ...     hostname='example.com')
        ...
        >>>
        """
        super(DjangoTrendingClient, self).__init__(*args, **kwargs)
        self.in_bulk = in_bulk_method
        self.fallback = fallback_method

    def get(self, site, offset=None, limit=None):
        """gets data from a corresponding trends table; sets `self.data` to a list of `Trend` objects; returns
        a list of model instances that either originated from the passed `in_bulk` or `fallback`

        :param site: the site name corresponding to the table
        :type site: str

        :param offset: the number of minutes to go back to aggregate
        :type offset: int

        :param limit: the maximum number of results to return
        :type limit: int

        :return: a list of model instances
        :rtype: list
        """
        content_ids = super(DjangoTrendingClient, self).get(site, offset)
        if len(content_ids):
            bulk = self.in_bulk(content_ids)
            instances = []
            for obj in bulk.values():
                trend = self.data.get(obj.pk)
                if trend:
                    instances.append((obj, trend.score))
            instances = sorted(instances, key=lambda i: i[1], reverse=True)
            instances = [i[0] for i in instances]
        else:
            instances = [i for i in self.fallback()]
        if limit:
            return instances[:limit]
        return instances
