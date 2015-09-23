
from django.db import models
from django.db.models import Avg, Sum


class PromiseSummary(object):
    def __init__(self, accomplished=0, in_progress=0, no_progress=0,
                 total_progress=0):
        self.accomplished = accomplished
        self.in_progress = in_progress
        self.no_progress = no_progress
        self.total_progress = total_progress

    @property
    def total(self):
        total = 0
        total += self.accomplished
        total += self.in_progress
        total += self.no_progress
        return total

    def calculate_percentage(self, number):
        if not self.total:
            return 0
        return (float(number)/float(self.total)) * 100

    @property
    def accomplished_percentage(self):
        return self.calculate_percentage(self.accomplished)

    @property
    def in_progress_percentage(self):
        return self.calculate_percentage(self.in_progress)

    @property
    def no_progress_percentage(self):
        return self.calculate_percentage(self.no_progress)


class PromiseQuerySet(models.query.QuerySet):
    def summary(self):
        summary = PromiseSummary()
        summary.no_progress = self.filter(
            fulfillment__percentage__exact=0).count()
        summary.accomplished = self.filter(
            fulfillment__percentage__exact=100).count()
        summary.in_progress = self.filter(
            fulfillment__percentage__range=(1, 99)).count()
        total_progress = 0
        ponderated = self.exclude(ponderator__isnull=True)
        not_ponderated = self.filter(ponderator__isnull=True)
        sum_ponderated = ponderated.aggregate(
            ponderator_sum=Sum('ponderator')).get('ponderator_sum') or 0
        default_ponderated = None
        if not_ponderated:
            default_ponderated = float(1 - sum_ponderated)/float(
                not_ponderated.count())
        ponderated_count = 0
        for promise in self.all():
            ponderator = promise.ponderator
            if promise.ponderator is None:
                ponderator = default_ponderated
                index = promise.fulfillment.percentage * ponderator
            else:
                index = promise.index
            total_progress += index
            ponderated_count += ponderator
        try:
            summary.total_progress = float(total_progress)/ponderated_count
        except ZeroDivisionError:
            summary.total_progress = 0
        return summary


class PromiseManager(models.Manager):
    def get_queryset(self):
        qs = PromiseQuerySet(self.model, using=self._db)
        return qs.annotate(percentage=Avg('fulfillment__percentage')).order_by(
            '-percentage', 'order')
