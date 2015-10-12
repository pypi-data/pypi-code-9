# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import (
    urlopen,
    Request,
)
from urlparse import urljoin
from re import compile as re_compile


class PyOGP(object):
    """
    """

    def __init__(self, **kwargs):
        """

        :param kwargs: options
            url: target url
            required_set:
            scrape: If scrape == True, then will try to fetch missing attributes
            db_host: Database host for cache
            db_port: Database port
            db_user: Database username
            db_password: Database user password
        :return:
        """
        self.result = {}
        self.cache = None

        if 'url' in kwargs:
            self.url = kwargs['url']

        if 'required_set' in kwargs:
            self.required_set = kwargs['required_set']
        else:
            self.required_set = {'title', 'description', 'image'}

        if 'scrape' in kwargs:
            self.scrape = kwargs['scrape']
        else:
            self.scrape = False


    def crawl(self, url, force_reload=False):
        """

        :param url:
        :return:
        """

        if self.cache and not force_reload:
            cached_data = self.cache.get_cached_data(url)
            if cached_data:
                self.result.update(cached_data)
                return self

        request = self._create_request(url)
        response = urlopen(request)
        encoding = self._get_encoding(response)
        self.soup = BeautifulSoup(response, from_encoding=encoding)
        self._get_ogp_meta()

        if self._is_complete():
            if self.cache:
                self.cache.put_data(url, self.result)
            return self  #complete getting required_set

        if 'description' not in self.result:
            self._get_description_meta()

        if self.soup.frameset:
            frame_tags = self.soup.frameset.find_all('frame')
            for frame in frame_tags:
                src = frame.attrs['src']
                self.crawl(self._get_absolute_url(url, src))
        # else: # if html does not have frame tag

        if 'title' not in self.result: # frame안에 og:title을 지키고있으면 일반적으로 <title>의 내용 보다 좋음
            content = self.soup.head.title.text
            if content: self.result['title'] = content # if content is not null.
        
        if self.cache:
            self.cache.put_data(url, self.result)

        return self

    def _get_ogp_meta(self):
        head = self.soup.html.head
        if head:
            ogp_meta_tags = head.find_all(property=re_compile(r'^og'))
        else:
            ogp_meta_tags = self.soup.html.find_all(property=re_compile(r'^og'))

        for meta in ogp_meta_tags:
            if meta.has_attr(u'content'):
                property_ = meta.attrs[u'property'][3:]  # cut off 'og:'
                if (property_ in self.required_set) and (property_ not in self.result):
                    content = meta.get('content',False)
                    if content:
                        self.result[property_] = content # content value not empty

    def _is_complete(self):
        """

        :return:
        """
        return set(self.result.viewkeys()) == self.required_set  # required_set을 다 찾으면

    def _get_description_meta(self):
        """
        get description by meta without og:description
        case : <meta name="description" content="...">
        :return:
        """
        description_meta_tags = self.soup.html.head.find_all(name='meta',
                                                             attrs={"name": ("description",
                                                                             "DC.description",
                                                                             "Description")
                                                                    },
                                                             )
        for meta in description_meta_tags:
            content_ = meta.get('content', False)
            if content_:
                self.result['description'] = content_

    def _create_request(self, url):
        """

        :param url:
        :return:
        """
        url = urlopen(url).geturl()  # get redirected url
        request = Request(url)
        request.add_header('User-Agent', 'Chrome')
        request.add_header('Referer', url)
        return request

    def _get_absolute_url(self, url, src):
        """
        get abosloute url from relative url(eg src value starts with '/foo')
        :param url:
        :param src:
        :return:
        """
        return urljoin(url, src)

    def _get_encoding(self, response):
        """

        :param response:
        :return:
        """
        encoding = 'utf-8'
        if 'Content-Type' in response.headers:
            content_types = response.headers.get('Content-Type').split(';')
            for c in content_types:
                if c.strip().startswith('charset'):
                    encoding = c.split('=')[1].strip()
                    break
        return encoding

    def get_soup(self):
        if hasattr(self, 'soup'):
            return self.soup
        else:
            raise AttributeError('Soup not exists. You have to call crawl() first.')




