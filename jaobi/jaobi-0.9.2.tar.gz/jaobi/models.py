# -*- coding: utf-8 -*-

import datetime
from uuid import uuid4
from tornado import gen, ioloop
from mongomotor import signals
from mongomotor import Document, EmbeddedDocument
from mongomotor.fields import (StringField, ReferenceField, BooleanField,
                               DateTimeField, ListField, UUIDField,
                               EmbeddedDocumentField, URLField)
from pyrocumulus.conf import settings
import resumeai
from jaobi.fields import SanitizedStringField
from jaobi.utils import generate_collection_scores


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

    @gen.coroutine
    def get_last_consumers(self, quantity=50):
        """
        Returns the last consumers of a content
        """
        content = yield ContentConsumption.objects.filter(content=self).\
            order_by('-inclusion_date')[:quantity]
        content = yield content.to_list()

        # it's kinda wierd thing, but I want to return
        # a queryset, so its the why of the .filter
        ids = []
        for c in content:
            ids.append((yield c.consumer).id)
        consumers = Consumer.objects.filter(id__in=ids)
        return consumers

    def __repr__(self):  # pragma no cover
        return 'content: %s' % self.title

    meta = {'allow_inheritance': True}


class Content(BaseContent):
    body = SanitizedStringField()
    summary = SanitizedStringField()

    @gen.coroutine
    def save(self, *args, **kwargs):

        if not self.summary and self.body is not None:
            if hasattr(settings, 'USE_RESUMEAI') and settings.USE_RESUMEAI:
                self.summary = resumeai.summarize_text(self.body).summary

        yield super().save(*args, **kwargs)


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
            c = yield c  # pragma: no cover
            content = yield c.content
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
        return ContentConsumption.objects.filter(consumer=self)

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

        if exclude:
            try:
                excluded_content = yield Content.objects.get(url=exclude)
            except Content.DoesNotExist:
                pass

        for consumer in similar_consumers:
            consumption = consumer.consumption()
            if excluded_content:
                consumption = consumption.filter(content__ne=excluded_content)
            for content in (yield self.consumption().to_list()):
                consumption = consumption.filter(
                    content__ne=content.content)

            ordered_consumption = yield consumption.order_by(
                '-consumption_date').to_list()
            for content in ordered_consumption:
                content = yield content.content
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

        for future in (yield self.consumption()[:depth]):
            # coverage does not feel good with coroutines, I think.
            # It show this line as not cover, but the next one yes.
            content_consumption = yield future  # pragma: no cover
            if not content_consumption:
                continue
            content = yield content_consumption.content
            if not content:
                continue
            for c in (yield content.get_last_consumers(
                    depth)).filter(id__ne=self.id):
                consumer = yield c
                if not consumer:
                    continue
                total += 1
                consumer_coincidence = consumers.get(str(consumer.id)) or 0
                consumer_coincidence += 1
                consumers[str(consumer.id)] = consumer_coincidence
        similar_consumers = generate_collection_scores(consumers, total)
        similar_consumers = [s[1] for s in similar_consumers[:quantity]]
        similar = yield type(self).objects.filter(
            id__in=similar_consumers).to_list()
        return sorted(similar,
                      key=lambda s: similar_consumers.index(str(s.id)))


class ContentConsumption(Document):
    content = ReferenceField(Content, required=True)
    # themes are here to easy reports.
    themes = ListField(StringField())
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

        yield super(ContentConsumption, self).save(*args, **kwargs)


loop = ioloop.IOLoop.instance()


@gen.coroutine
def ensure_index():
    yield ContentConsumption.ensure_index('consumer')
    yield ContentConsumption.ensure_index('content')
    yield ContentConsumption.ensure_index('-inclusion_date')

loop.run_sync(ensure_index)
