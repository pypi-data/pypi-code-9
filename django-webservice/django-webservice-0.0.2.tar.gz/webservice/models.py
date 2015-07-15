import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


SYNCHRONIZED_MODEL_FIELDS = ("uuid", "status")


class SynchronizedQuerySet(models.query.QuerySet):
    def delete(self):
        # can be a performance issue, but we need to be clear about the status
        for model in self.all():
            model.delete()


class SynchronizedManager(models.Manager):
    def get_queryset(self):
        return SynchronizedQuerySet(self.model, using=self._db)


class SynchronizedModel(models.Model):
    class Meta:
        abstract = True

    objects = SynchronizedManager()

    STATUS_DRAFT = 1
    STATUS_PUBLISHED = 2
    STATUS_PUBLISHED_DRAFT = 3
    STATUS_PUBLISHED_DELETED = 4

    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_PUBLISHED, _('Published')),
        (STATUS_PUBLISHED_DRAFT, _('Published Draft')),
        (STATUS_PUBLISHED_DELETED, _('Published Deleted')),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_DRAFT)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        else:
            # ugly but for now it must be sufficient...
            if self.status == SynchronizedModel.STATUS_DRAFT:
                old = self.__class__.objects.get(pk=self._get_pk_val())
                self.status = SynchronizedModel.STATUS_PUBLISHED_DRAFT \
                    if old.status != SynchronizedModel.STATUS_DRAFT else self.status
        self.updated = timezone.now()
        return super(SynchronizedModel, self).save(*args, **kwargs)

    def delete(self, using=None):
        if self.status == SynchronizedModel.STATUS_DRAFT:
            return super(SynchronizedModel, self).delete(using=using)
        self.status = SynchronizedModel.STATUS_PUBLISHED_DELETED
        return self.save(using=using)

    def reload(self):
        new_self = self.__class__.objects.get(pk=self.pk)
        # You may want to clear out the old dict first or perform a selective merge
        self.__dict__.update(new_self.__dict__)

    @property
    def is_deleted(self):
        return self.status in (SynchronizedModel.STATUS_PUBLISHED_DELETED, SynchronizedModel.STATUS_PUBLISHED_DRAFT)


class I18NForeignKey(models.ForeignKey):
    def __init__(self, to, to_field=None, rel_class=models.ManyToOneRel,
                 db_constraint=True, **kwargs):
        kwargs["related_name"] = "contents"
        super(I18NForeignKey, self).__init__(to, to_field=to_field, rel_class=rel_class, db_constraint=db_constraint,
                                             **kwargs)


class ContentModel(models.Model):
    class Meta:
        abstract = True
        unique_together = ('base_model', 'language',)

    language = models.CharField(choices=settings.LANGUAGES, default=settings.LANGUAGES[0][0], max_length=5)

    def save(self, *args, **kwargs):
        super(ContentModel, self).save(args, kwargs)
        if self.base_model is not None:
            self.base_model.save()