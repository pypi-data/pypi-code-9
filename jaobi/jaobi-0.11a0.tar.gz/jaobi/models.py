# -*- coding: utf-8 -*-

import datetime
from uuid import uuid4
from bson.dbref import DBRef
from tornado import gen, ioloop
from mongomotor import signals
from mongomotor import Document, EmbeddedDocument
from mongomotor.fields import (StringField, ReferenceField, BooleanField,
                               DateTimeField, ListField, UUIDField,
                               EmbeddedDocumentField, URLField)
from pyrocumulus.conf import settings
import resumeai
from jaobi.fields import SanitizedStringField
from jaobi.utils import generate_collection_scores, log


class BaseContent(Document):
    url = URLField(required=True, unique=True)
    image = URLField()
    themes = ListField(StringField())
    title = SanitizedStringField(required=True)
    description = SanitizedStringField()
    publication_date = DateTimeField(required=True)
    # wich site published this content
    origin = StringField()
    # what organization produced it. A producer can be a
    # 'hub' of origins
    producer = StringField()

    @gen.coroutine
    def save(self, *args, **kwargs):
        if not self.publication_date:
            self.publication_date = datetime.datetime.now()
        yield super(BaseContent, self).save(*args, **kwargs)

    def __repr__(self):  # pragma no cover
        return 'content: %s' % self.title

    meta = {'allow_inheritance': True}


class Content(BaseContent):
    body = SanitizedStringField()
    summary = SanitizedStringField()
    recomends = BooleanField(default=True, required=True)
    last_consumers = ListField(StringField())

    @gen.coroutine
    def save(self, *args, **kwargs):

        if not self.summary and self.body is not None:
            if hasattr(settings, 'USE_RESUMEAI') and settings.USE_RESUMEAI:
                self.summary = resumeai.summarize_text(self.body).summary

        yield super().save(*args, **kwargs)

    def get_last_consumers(self):
        """
        Returns the last consumers of a content
        """

        consumers = Consumer.objects.filter(id__in=self.last_consumers)
        return consumers

    @classmethod
    @gen.coroutine
    def post_content_consumption_save(cls, sender, document, **kwargs):
        consumer = yield document.consumer
        content = yield document.content

        try:
            last_consumers = content.last_consumers
        except AttributeError:
            log('content as dbref for content last consumer',
                level='error')
            return

        last_consumers.insert(0, str(consumer.id))

        last_consumers = last_consumers[:settings.CONSUMPTION_HISTORY_SIZE]
        yield content.update(last_consumers=last_consumers)

    @classmethod
    @gen.coroutine
    def bulk_post_content_consumption_save(cls, sender, documents, **kwargs):

        for document in documents:
            yield cls.post_content_consumption_save(sender, document, **kwargs)


class ConsumerProfile(EmbeddedDocument):
    parent_doc = ReferenceField('Consumer', required=True)

    @gen.coroutine
    def get_preferred_themes(self):
        themes_hits = {}
        queryset = (yield self.parent_doc).consumption()
        total_hits = yield queryset.count()
        for c in queryset:
            # coverage does not feel good with coroutines, I think.
            # It show this line as not cover, but the next one yes.
            content = yield c  # pragma: no cover
            if not content:
                continue
            themes = content.themes
            for theme in themes:
                theme_hits = themes_hits.get(str(theme)) or 0
                theme_hits += 1
                themes_hits[str(theme)] = theme_hits
        preferred = generate_collection_scores(themes_hits, total_hits)
        return preferred


class Consumer(Document):
    uuid = UUIDField()
    profile = EmbeddedDocumentField(ConsumerProfile)
    creation_date = DateTimeField()
    last_consumption = ListField(StringField())

    def __repr__(self):  # pragma: no cover
        return 'consumer: %s' % self.id

    @gen.coroutine
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid4())
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()

        yield super(Consumer, self).save(*args, **kwargs)
        if not self.profile:
            self.profile = ConsumerProfile(parent_doc=self)
            yield super(Consumer, self).save(*args, **kwargs)

    def consumption_history(self):
        return ContentConsumption.objects.filter(consumer=self, consumed=True)

    def future_consumption(self):
        return ContentConsumption.objects.filter(consumer=self, consumed=False)

    def consumption(self):
        return Content.objects.filter(url__in=self.last_consumption)

    @gen.coroutine
    def get_suggestions(self, quantity=20, depth=50, profile_depth=5,
                        exclude=None, similar_ids=None):
        """Returns content suggestions.

        :param quantity: How many suggestions should be returned
        :param depth: How many contents will be considered in each consumer
          profile
        :param profile_depth: How many profiles will be checked
        :param exclude: An url of a content to be excluded. """

        if similar_ids:
            similar_consumers = yield type(self).objects.filter(
                id__in=similar_ids).to_list()
        else:
            similar_consumers = yield self.get_similar_consumers(depth,
                                                                 profile_depth)
        candidate_content = yield self.get_candidate_content(
            similar_consumers, quantity, exclude=exclude)
        return candidate_content

    @gen.coroutine
    def get_candidate_content(self, similar_consumers, quantity, exclude=None):
        """ Returns content that may be suggested.

        :param similar_consumers: A list with consumers ids with similar
          profile.
        :param quantity: How many contents should be returned.
        :param exclude: An url of a content to be excluded."""

        candidate_content = []
        excluded_content = None

        for consumer in similar_consumers:
            consumption = consumer.consumption()
            if exclude:
                consumption = consumption.filter(url__ne=exclude)
            for content in (yield self.consumption().to_list()):
                consumption = consumption.filter(url__ne=content.url)

            ordered_consumption = yield consumption.order_by(
                '-consumption_date').to_list()
            for content in ordered_consumption:
                if not content.recomends:
                    continue
                if content not in candidate_content:  # pragma: no cover
                    candidate_content.append(content)
                if len(candidate_content) == quantity:
                    break
            if len(candidate_content) == quantity:
                break
        return candidate_content

    @gen.coroutine
    def get_similar_consumers(self, quantity, depth):
        consumers = {}
        total = 0
        consumption = yield self.consumption().filter(
            last_consumers__ne=self.id).limit(depth)
        consumers = yield consumption.item_frequencies('last_consumers')
        try:
            del consumers[str(self.id)]
        except KeyError:
            pass
        total = sum([v for k, v in consumers.items()])

        similar_consumers = generate_collection_scores(consumers, total)
        similar_consumers = [s[1] for s in similar_consumers[:quantity]]
        similar = yield type(self).objects.filter(
            id__in=similar_consumers).to_list()
        return sorted(similar,
                      key=lambda s: similar_consumers.index(str(s.id)))

    @classmethod
    @gen.coroutine
    def post_content_consumption_save(cls, sender, document, **kwargs):
        consumer = yield document.consumer
        content = yield document.content

        try:
            consumer.last_consumption.insert(0, content.url)
        except AttributeError:
            log('consumer as dbref for consumer last consumption',
                level='error')
            return

        consumer.last_consumption = consumer.last_consumption[
            :settings.CONSUMPTION_HISTORY_SIZE]
        yield consumer.save()

    @classmethod
    @gen.coroutine
    def bulk_post_content_consumption_save(cls, sender, documents, **kwargs):
        for document in documents:
            yield cls.post_content_consumption_save(sender, document, **kwargs)


class ContentConsumption(Document):
    content = ReferenceField(Content, required=True)
    # themes and origin are here to easy reports.
    themes = ListField(StringField())
    origin = StringField()
    consumer = ReferenceField(Consumer, required=True)
    referrer = StringField()
    inclusion_date = DateTimeField()
    consumption_date = DateTimeField()
    unload_date = DateTimeField()
    consumed = BooleanField()

    @gen.coroutine
    def save(self, *args, **kwargs):
        if not self.inclusion_date:
            self.inclusion_date = datetime.datetime.now()
        if self.consumed and not self.consumption_date:
            self.consumption_date = datetime.datetime.now()

        self.themes = (yield self.content).themes
        self.origin = (yield self.content).origin

        yield super(ContentConsumption, self).save(*args, **kwargs)


loop = ioloop.IOLoop.instance()


@gen.coroutine
def ensure_index():
    yield ContentConsumption.ensure_index('consumer')
    yield ContentConsumption.ensure_index('content')
    yield ContentConsumption.ensure_index('-inclusion_date')
    yield ContentConsumption.ensure_index('origin')
    yield ContentConsumption.ensure_index('themes')
    yield ContentConsumption.ensure_index('referrer')

loop.run_sync(ensure_index)


signals.post_save.connect(Consumer.post_content_consumption_save,
                          sender=ContentConsumption)


signals.post_bulk_insert.connect(Consumer.bulk_post_content_consumption_save,
                                 sender=ContentConsumption)

signals.post_save.connect(Content.post_content_consumption_save,
                          sender=ContentConsumption)


signals.post_bulk_insert.connect(Content.bulk_post_content_consumption_save,
                                 sender=ContentConsumption)
