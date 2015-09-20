from __future__ import unicode_literals
from importlib import import_module

from django.utils.encoding import python_2_unicode_compatible
from django.db import models


@python_2_unicode_compatible
class Condition(models.Model):
    """
    Stores the details of a Python function which will be used to determine this condition's
    truthiness.
    """
    name = models.CharField(max_length=64)
    module = models.CharField(
        max_length=128, help_text="Module in which the condition function resides")
    function = models.CharField(
        max_length=64,
        help_text=("The function which returns True or False to determine the result of this "
                   "condition"))

    def __str__(self):
        return self.name

    def call(self, *args, **kwargs):
        """
        Imports and calls the condition function with the provided arguments and returns its
        response.
        """
        return getattr(import_module(self.module), self.function)(*args, **kwargs)


class Chain(models.Model):
    name = models.CharField(max_length=128)

    def call(self, *args, **kwargs):
        """
        Runs each condition and evaluates whether the entire condition chain has succeeded. Passes
        through any arguments provided to each Condition.
        """
        # Artificially set the first result to True to make our lives easier
        # when joining the rest of the conditions together.
        expression = "True"
        for element in self.elements_queryset:
            expression += " %s " % element.joiner.lower()
            expression += "%s" % bool(element.condition.call(*args, **kwargs))
        return eval(expression)

    def __iter__(self):
        return iter(self.elements_queryset)

    def __len__(self):
        return self.elements_queryset.count()

    def __getitem__(self, key):
        return self.elements_queryset[key]

    def __reversed__(self):
        return self.elements_queryset.order_by("-order")

    @property
    def elements_queryset(self):
        return ChainElement.objects.filter(chain=self).order_by("order")

    # @transaction.atomic
    # def append(self, element):
    #     """
    #     Update the element's chain property to be this Chain, and set its order
    #     to be the last in the current list of elements.
    #     """
    #     next_order = reversed(self).only("order")[0].order + 1
    #     element.chain = self
    #     element.order = 0
    #     element.save()
    #     ChainElement.objects.filter(pk=element.pk).update(order=next_order)


@python_2_unicode_compatible
class ChainElement(models.Model):
    links = (
        (u'and', u'and'),
        (u'or', u'or')
    )
    chain = models.ForeignKey(Chain)
    joiner = models.CharField(choices=links, max_length=3, default="and")
    negated = models.BooleanField(default=False)
    condition = models.ForeignKey(Condition)
    order = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (
            ("chain", "order"),
        )

    def __str__(self):
        isnt = "NOT " if self.negated else ""
        joiner = self.joiner if self.joiner else "IF"
        return "%s %s%s" % (joiner, isnt, self.condition)
