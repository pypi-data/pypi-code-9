from django.db import models
from popolo.models import Person, Identifier
from autoslug import AutoSlugField
from .queryset import PromiseManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=512)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    @property
    def fulfillment_percentage(self):
        sum_of_percentages = 0
        for promise in self.promises.all():
            sum_of_percentages += promise.fulfillment.percentage
        try:
            return sum_of_percentages / self.promises.count()
        except ZeroDivisionError:
            return 0

    def __unicode__(self):
        return self.name


class Promise(models.Model):
    name = models.CharField(max_length=2048)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    person = models.ForeignKey(Person, null=True, blank=True)
    category = models.ForeignKey(Category, related_name="promises", null=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    ponderator = models.FloatField(default=None, null=True, blank=True)
    identifiers = generic.GenericRelation(Identifier, help_text="Issued identifiers")
    tags = TaggableManager()

    objects = PromiseManager()

    class Meta:
        verbose_name = _("Promise")
        verbose_name_plural = _("Promises")

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super(Promise, self).save(*args, **kwargs)
        if creating:
            self.fulfillment = Fulfillment.objects.create(promise=self)

    @property
    def index(self):
        if self.ponderator is None:
            return None
        return self.fulfillment.percentage * self.ponderator

    def __unicode__(self):
        if self.person is None:
            return u"Someone promessed {what} with {percentage}%".format(
                what=self.name,
                percentage=self.fulfillment.percentage)
        return u"{who} promessed {what} with {percentage}%".format(
            who=self.person.name,
            what=self.name,
            percentage=self.fulfillment.percentage)


class ExternalDocumentMixin(models.Model):
    url = models.URLField()
    display_name = models.CharField(max_length=512)
    date = models.DateField(null=True)

    class Meta:
        abstract = True


class InformationSource(ExternalDocumentMixin):
    promise = models.ForeignKey(Promise, related_name='information_sources')

    class Meta:
        verbose_name = _("Information Source")
        verbose_name_plural = _("Information Sources")


class VerificationDocument(ExternalDocumentMixin):
    promise = models.ForeignKey(Promise, related_name='verification_documents',
                                null=True)

    class Meta:
        verbose_name = _("Verification Document")
        verbose_name_plural = _("Verification Documents")


class Fulfillment(models.Model):
    promise = models.OneToOneField(Promise)
    percentage = models.PositiveIntegerField(default=0)
    status = models.TextField(default="", blank=True)
    description = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = _("Fulfilment")
        verbose_name_plural = _("Fulfilments")


class Milestone(models.Model):
    promise = models.ForeignKey(Promise, related_name="milestones")
    date = models.DateField()
    description = models.TextField()

    def __unicode__(self):
        return u"{what} - {when}".format(what=self.description, when=self.date)

    class Meta:
        verbose_name = _("Milestone")
        verbose_name_plural = _("Milestones")
        ordering = ('date',)
