# -*- coding: utf-8 -*-

# In this module is the consolidated data for reports about
# Jaobi usage.

from collections import defaultdict
import datetime
from mongomotor import Document
from mongomotor import signals
from mongomotor.fields import StringField, IntField, DateTimeField, ListField
from tornado import gen
from jaobi.models import ContentConsumption
from jaobi.utils import log


@gen.coroutine
def update_themes_consolidation(cls, document):
    """Updates the consolidated theme reports for a given document."""

    today = datetime.date.today()
    themes = document.themes
    for theme in themes:
        kw = {'theme': theme, 'day': today}
        try:
            consolidated = yield cls.objects.get(**kw)
        except cls.DoesNotExist:
            consolidated = cls(**kw)
            yield consolidated.save()

        consolidated.total += 1
        yield consolidated.save()


@gen.coroutine
def get_consolidation(cls, key, **kwargs):
    qs = cls.objects.filter(**kwargs).only(key, 'total')
    qslist = yield qs.to_list()
    consolidation = defaultdict(int)
    for consumption in qslist:
        consumption_key = getattr(consumption, key)
        consolidation[consumption_key] += consumption.total
    return consolidation


@gen.coroutine
def get_consolidation_history(cls, key, **kwargs):
    qs = cls.objects.filter(**kwargs).only(key, 'total', 'day')
    qs = qs.order_by('-day')
    qslist = yield qs.to_list()
    consolidation = defaultdict(list)
    for consumption in qslist:
        consumption_key = getattr(consumption, key)
        consolidation[consumption_key].append({'day': consumption.day,
                                               'total': consumption.total})
    return consolidation


class ThemeDailyConsumption(Document):

    theme = StringField(required=True)
    day = DateTimeField(required=True, unique_with='theme')
    total = IntField(default=0, required=True)

    @classmethod
    @gen.coroutine
    def update_consumption(cls, sender, document, **kwargs):

        yield update_themes_consolidation(cls, document)

    @classmethod
    @gen.coroutine
    def get_consumption(cls, **kwargs):
        consumption = yield get_consolidation(cls, 'theme', **kwargs)
        return consumption

    @classmethod
    @gen.coroutine
    def get_consumption_history(cls, **kwargs):
        consumption = yield get_consolidation_history(cls, 'theme', **kwargs)
        return consumption

    @classmethod
    @gen.coroutine
    def bulk_update_consumption(cls, sender, documents, **kwargs):
        for document in documents:
            yield cls.update_consumption(sender, document, **kwargs)


class ThemeDailyConsumers(Document):
    theme = StringField(required=True)
    day = DateTimeField(required=True, unique_with='theme')
    consumers = ListField(StringField())
    total = IntField(default=0, required=True)

    @classmethod
    @gen.coroutine
    def update_consumers(cls, sender, document, **kwargs):
        today = datetime.date.today()
        themes = document.themes
        consumer = yield document.consumer

        for theme in themes:
            kw = {'theme': theme, 'day': today}
            try:
                consolidated = yield cls.objects.get(**kw)
            except cls.DoesNotExist:
                consolidated = cls(**kw)
                yield consolidated.save()

            if str(consumer) in consolidated.consumers:
                log('consumer {} already on theme {} {}'.format(
                    consumer, theme, today), level='warning')
                continue

            consolidated.consumers.append(str(consumer))
            consolidated.total += 1
            yield consolidated.save()

    @classmethod
    @gen.coroutine
    def bulk_update_consunsumers(cls, sender, documents, **kwargs):
        for document in documents:
            yield cls.update_consumers(sender, document, **kwargs)

    @classmethod
    @gen.coroutine
    def get_consumers(cls, **kwargs):
        consumption = yield get_consolidation(cls, 'theme', **kwargs)
        return consumption

    @classmethod
    @gen.coroutine
    def get_consumers_history(cls, **kwargs):
        consumption = yield get_consolidation_history(cls, 'theme', **kwargs)
        return consumption

    @classmethod
    @gen.coroutine
    def clean_old_days(cls, sender, document, **kwargs):
        """ Removes info from past days to save space."""

        today = datetime.datetime.today()
        today = datetime.datetime(today.year, today.month, today.day,
                                  0, 0, 0)
        qslist = yield cls.objects.filter(day__lt=today).to_list()
        for item in qslist:
            yield item.update(set__consumers=[])


class ReferrerDailyConsumption(Document):
    referrer = StringField(required=True)
    day = DateTimeField(required=True, unique_with='referrer')
    total = IntField(default=0, required=True)

    @classmethod
    @gen.coroutine
    def update_consumption(cls, sender, document, **kwargs):
        if not document.referrer:
            return
        today = datetime.date.today()
        kw = {'referrer': document.referrer, 'day': today}
        try:
            consolidated = yield cls.objects.get(**kw)
        except cls.DoesNotExist:
            consolidated = cls(**kw)
            yield consolidated.save()

        consolidated.total += 1
        yield consolidated.save()

    @classmethod
    @gen.coroutine
    def bulk_update_consumption(cls, sender, documents, **kwargs):
        for document in documents:
            yield cls.update_consumption(sender, document, **kwargs)

    @classmethod
    @gen.coroutine
    def get_consumption(cls, **kwargs):
        consumption = yield get_consolidation(cls, 'referrer', **kwargs)
        return consumption

    @classmethod
    @gen.coroutine
    def get_consumption_history(cls, **kwargs):
        consumption = yield get_consolidation_history(cls, 'referrer', **kwargs)
        return consumption


class OriginDailyConsumption(Document):
    origin = StringField(required=True)
    day = DateTimeField(required=True, unique_with='origin')
    total = IntField(default=0, required=True)

    @classmethod
    @gen.coroutine
    def update_consumption(cls, sender, document, **kwargs):
        origin = document.origin
        if not origin:
            msg = 'no origin for content consumption {}'.format(
                str(document.id))
            log(msg, level='error')
            return

        today = datetime.date.today()
        kw = {'origin': origin, 'day': today}
        try:
            consolidated = yield cls.objects.get(**kw)
        except cls.DoesNotExist:
            consolidated = cls(**kw)
            yield consolidated.save()

        consolidated.total += 1
        yield consolidated.save()

    @classmethod
    @gen.coroutine
    def bulk_update_consumption(cls, sender, documents, **kwargs):

        for document in documents:
            yield cls.update_consumption(sender, document, **kwargs)

    @classmethod
    @gen.coroutine
    def get_consumption(cls, **kwargs):
        consumption = yield get_consolidation(cls, 'origin', **kwargs)
        return consumption

    @classmethod
    @gen.coroutine
    def get_consumption_history(cls, **kwargs):
        consumption = yield get_consolidation_history(cls, 'origin', **kwargs)
        return consumption


class ConsumptionAverageTime(Document):
    theme = StringField(required=True)
    day = DateTimeField(required=True, unique_with='theme')
    average = IntField(default=0, required=True)
    total = IntField(default=0, required=True)
    access_count = IntField(default=0, required=True)

    @gen.coroutine
    def save(self, *args, **kwargs):
        if self.access_count > 0:
            self.average = self.total / self.access_count

        yield super().save(*args, **kwargs)

    @classmethod
    @gen.coroutine
    def update_consumption(cls, sender, document, **kwargs):
        if not document.unload_date:
            return

        today = datetime.date.today()
        themes = document.themes
        for theme in themes:
            kw = {'theme': theme, 'day': today}
            try:
                consolidated = yield cls.objects.get(**kw)
            except cls.DoesNotExist:
                consolidated = cls(**kw)
                yield consolidated.save()

            if document.unload_date and document.consumption_date:
                consumption_time = (document.unload_date -
                                    document.consumption_date)
            else:
                consumption_time = datetime.timedelta(seconds=1)
            consolidated.total += consumption_time.seconds
            consolidated.access_count += 1
            yield consolidated.save()

    @classmethod
    @gen.coroutine
    def bulk_update_consumption(cls, sender, documents, **kwargs):

        for document in documents:
            yield cls.update_consumption(sender, document, **kwargs)

    @classmethod
    @gen.coroutine
    def get_average_consumption(cls, **kwargs):
        qs = cls.objects.filter(**kwargs)
        themes_count = defaultdict(int)
        consolidation = defaultdict(int)
        for future in qs:
            consumption = yield future
            if not consumption:
                continue
            themes_count[consumption.theme] += 1
            consolidation[consumption.theme] += consumption.average

        for theme, count in themes_count.items():
            consolidation[theme] = consolidation[theme] / count

        return consolidation


signals.post_save.connect(ThemeDailyConsumption.update_consumption,
                          sender=ContentConsumption)

signals.post_bulk_insert.connect(
    ThemeDailyConsumption.bulk_update_consumption,
    sender=ContentConsumption)

signals.post_save.connect(ThemeDailyConsumers.update_consumers,
                          sender=ContentConsumption)

signals.post_save.connect(ThemeDailyConsumers.clean_old_days,
                          sender=ThemeDailyConsumers)

signals.post_bulk_insert.connect(
    ThemeDailyConsumers.bulk_update_consunsumers,
    sender=ContentConsumption)

signals.post_save.connect(ReferrerDailyConsumption.update_consumption,
                          sender=ContentConsumption)

signals.post_bulk_insert.connect(
    ReferrerDailyConsumption.bulk_update_consumption,
    sender=ContentConsumption)

signals.post_save.connect(OriginDailyConsumption.update_consumption,
                          sender=ContentConsumption)

signals.post_bulk_insert.connect(
    OriginDailyConsumption.bulk_update_consumption,
    sender=ContentConsumption)


signals.post_save.connect(ConsumptionAverageTime.update_consumption,
                          sender=ContentConsumption)

signals.post_bulk_insert.connect(
    ConsumptionAverageTime.bulk_update_consumption,
    sender=ContentConsumption)
