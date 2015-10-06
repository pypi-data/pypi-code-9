# -*- coding: utf-8 -*-

from datetime import datetime
import tornado
from tornado import gen
from pyrocumulus.web.applications import (Application, RestApplication,
                                          StaticApplication, URLSpec)
from mongoengine.errors import ValidationError
from mongoengine.queryset import NotUniqueError
from pyrocumulus.web.decorators import get, put, post, options
from pyrocumulus.web.handlers import RestHandler, TemplateHandler, HTTPError
from pyrocumulus.conf import settings

import jaobi
from jaobi.cache import get_cache
from jaobi.models import (Content, Consumer, ContentConsumption)
from jaobi.reports import (ThemeDailyConsumers, ThemeDailyConsumption,
                           ReferrerDailyConsumption)
from jaobi.utils import log


class JaobiRestHandler(RestHandler):

    @gen.coroutine
    def prepare(self):
        self.check_api_key()
        yield super(JaobiRestHandler, self).prepare()
        try:
            del self.params['api_key']
        except KeyError:
            pass

    def check_api_key(self):
        if self.request.method == 'OPTIONS':
            return
        api_key = self.request.arguments.get('api_key')
        try:
            del self.request.arguments['api_key']
        except KeyError:
            pass

        if api_key:
            api_key = api_key[0].decode()

        domain = self._get_domain(self.request.headers.get("Referer"))

        is_valid = self._is_valid_key(api_key, domain)
        if not is_valid:
            msg = '[403] key: {} domain: {}\n'.format(api_key, domain)
            raise HTTPError(403, msg)

    def _is_valid_key(self, api_key, domain):
        if (not api_key or
            (not self._is_secret_key(api_key)
             and not self._is_valid_domain_key(api_key, domain))):
            return False

        return True

    def _is_secret_key(self, api_key):
        skey = settings.SECRET_API_KEY
        return api_key == skey

    def _is_valid_domain_key(self, api_key, domain):
        domains = settings.DOMAIN_KEYS.get(api_key, [])
        return domain in domains

    def _get_domain(self, uri):
        if not uri:
            return
        domain = uri.split('http://')[1].split('/')[0].replace('www.', '')
        return domain


class ConsumerRestHandler(JaobiRestHandler):

    """
    Rest RequestHandler for Consumer improved with
    behavioral content suggestion
    """

    # hack!! someone dropped the database that was used
    # in production, but lots of users already has
    # their eternal cookies from interphone, meaning
    # this was fucking the system!
    @gen.coroutine
    def _get_consumer(self, consumer_id):  # pragma no coverage for hacks!
        try:
            consumer = yield self.model.objects.get(id=consumer_id)
        except self.model.DoesNotExist:
            consumer = self.model(id=consumer_id)
            yield consumer.save()

        return consumer

    @gen.coroutine
    def prepare(self):
        self.similar_consumers = self.request.arguments.get('s') or []

        yield super(ConsumerRestHandler, self).prepare()
        # the != 'undefined' is because the js is sending undefined as id
        # for similar_consumers sometimes. Need to correct the js.
        self.similar_consumers = [s.decode() for s in self.similar_consumers
                                  if s.decode() != 'undefined']

    @get('similar-consumers')
    @gen.coroutine
    def get_similar_consumers(self, **kwargs):
        """
        Returns consumers with a similar navigation history
        """
        consumer = yield self._get_consumer(self.params['consumer_id'])
        quantity = self.params.get('quantity') or 5
        quantity = int(quantity)
        depth = 20
        content = yield consumer.get_similar_consumers(quantity, depth)
        extra = {'items_returned': len(content)}
        self.json_extra_params.update(extra)
        return content

    @get('behavioral-suggestions')
    @gen.coroutine
    def get_suggestions(self, **kwargs):
        """
        Returns content suggestion based on similar consumers, consumers with
        similar navigation history.
        """
        try:
            consumer = yield self._get_consumer(self.params['consumer_id'])
        except ValidationError:
            raise HTTPError(500, 'bad consumer_id for suggestions')

        quantity = self.params.get('quantity') or 5
        quantity = int(quantity)
        uri = self.params.get('content_uri')

        content = yield consumer.get_suggestions(
            quantity, exclude=uri, similar_ids=self.similar_consumers)

        extra = {'items_returned': len(content)}
        self.json_extra_params.update(extra)
        return content

    @get('preferred-themes')
    @gen.coroutine
    def get_preferred_themes(self, **kwargs):
        consumer = yield self._get_consumer(self.params['consumer_id'])
        preferred = yield consumer.profile.get_preferred_themes()
        preferred = {'items': preferred}
        return preferred

    @put('create')
    @options('create')
    @gen.coroutine
    def create_consumer(self, **kwargs):
        consumer = self.model()
        yield consumer.save()
        return consumer


class ContentRestHandler(JaobiRestHandler):

    """
    Rest RequestHandler for Content improved with
    list of last consumers
    """

    @get('last-consumers')
    @gen.coroutine
    def get_last_consumers(self, **kwargs):
        content_url = self.params['url']
        quantity = self.params.get('quantity') or 20
        quantity = int(quantity)
        try:
            content = yield self.model.objects.get(url=content_url)
        except self.model.DoesNotExist:  # pragma no coverage for hacks!
            # hack for dropped database
            return {}

        last_consumers = yield content.get_last_consumers(quantity)
        count = yield last_consumers.count()
        extra = {'items_returned': count}
        self.json_extra_params.update(extra)
        return last_consumers

    @put('')
    @post('')
    @gen.coroutine
    def put_object(self):
        obj = self.model(**self.params)
        try:
            yield obj.save()
        except NotUniqueError:
            obj = yield self.model.objects.get(url=self.params['url'])
            for k, v in self.params.items():
                setattr(obj, k, v)
            yield obj.save()

        return obj


class ContentConsumptionHandler(JaobiRestHandler):

    @gen.coroutine
    def _recover_content(self):
        # Sometimes I get a valid url of a content, but the content
        # is not on the database (usualy because of dropped old stuff),
        # so in order to not lose the consumption I try to save this
        # thigs to database.

        content_url = self.request.arguments.get(
            'content__url', [b''])[0].decode()

        if not content_url:
            raise HTTPError(500, 'no content for consumption')

        origin = self._get_domain(content_url)
        content = Content(url=content_url, title='bad-content-title',
                          recomends=False, origin=origin)
        yield content.save()
        self.params['content'] = content
        log('content recovered {}'.format(content_url), level='warning')

    @gen.coroutine
    def _recover_consumer(self, new_id=False):
        # Here is the samething that happens with content.
        consumer_id = self.request.arguments.get(
            'consumer__id', [b''])[0].decode()

        if not consumer_id:
            raise HTTPError(500, 'no consumer for consumption')

        kw = {'id': consumer_id}
        if new_id:
            kw = {}

        consumer = Consumer(**kw)
        yield consumer.save()
        self.params['consumer'] = consumer

    @gen.coroutine
    def prepare(self):

        try:
            yield super(ContentConsumptionHandler, self).prepare()
        except ValidationError:
            raise HTTPError(500, 'bad content consumption')

    @post('put')
    @post('')
    @put('')
    @gen.coroutine
    def put_object(self):
        """
        Insert a new ContentConsumption. Associates the themes of the content
        with the consumption.
        """
        obj = self.model(**self.params)
        # doing it here so the themes are correct even if using cache.
        obj.inclusion_date = datetime.now()
        obj.consumption_date = datetime.now()

        if not self.params.get('content'):
            yield self._recover_content()

        if not self.params.get('consumer'):
            yield self._recover_consumer()

        try:
            obj.themes = self.params['content'].themes
            obj.origin = self.params['content'].origin
        except AttributeError:
            msg = 'wierd content consumption. no content or consumption '
            url = self.request.arguments.get('content__url', [b''])[0].decode()
            cid = self.request.arguments.get('consumer__id', [b''])[0].decode()
            msg += 'on params. {} {}'.format(url, cid)
            raise HTTPError(500, msg)

        if settings.USE_CONSUMPTION_CACHE:
            cache = get_cache()
            tornado.ioloop.IOLoop.instance().spawn_callback(cache.add, obj)
        else:
            try:
                yield obj.save()
            except AttributeError:  # pragma no coverage for hacks!
                # dropped db shit
                return {}

        return obj

    @post('consumption-finished')
    @put('consumption-finished')
    @gen.coroutine
    def consumption_finished(self):
        content = self.params['content']
        consumer = self.params['consumer']
        consumption = yield self.model.objects.filter(
            content=content, consumer=consumer).order_by(
                '-consumption_date')[0]
        consumption.unload_date = datetime.now()
        yield consumption.save()
        return consumption

    @get('by-theme')
    @gen.coroutine
    def get_consumption_by_theme(self):
        by_theme = yield ThemeDailyConsumption.get_consumption(**self.params)

        return by_theme

    @get('by-referrer')
    @gen.coroutine
    def get_consumption_by_referrer(self):
        kw = self.params
        kw.update({'referrer__ne': None})
        by_referrer = yield ReferrerDailyConsumption.get_consumption(
            **kw)

        return by_referrer

    @get('consumers-by-theme')
    @gen.coroutine
    def get_consumers_by_theme(self):
        by_theme = yield ThemeDailyConsumers.get_consumers(**self.params)
        return by_theme


class InterfoneTemplateHandler(TemplateHandler):

    def get(self):
        template = 'consumer_server.html'
        extra_context = {'STATIC_URL': settings.STATIC_URL}
        self.render_template(template, extra_context)


class PlaceHolder(TemplateHandler):  # pragma: no cover

    def get(self):
        txt = """
jao.bi

version: %s
""" % (jaobi.VERSION)
        self.write(txt)


base_rest_app = RestApplication(ContentConsumption, Consumer, Content)

static_app = StaticApplication()

url = URLSpec('/interfone/consumer_server.html$', InterfoneTemplateHandler)
placeholder = URLSpec('/', PlaceHolder)
template_app = Application(url_prefix='', handlerfactory=lambda: None,
                           extra_urls=[url, placeholder])
