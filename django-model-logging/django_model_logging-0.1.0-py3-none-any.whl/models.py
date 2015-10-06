from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from pgcrypto.fields import TextPGPPublicKeyField


def get_model_path(model):
    """Return the qualified path to a model class: 'model_logging.models.LogEntry'."""
    return '{}.{}'.format(model.__module__, model.__qualname__)


class LogEntryManager(models.Manager):
    def log(self, log_entry_creator, operation, model, user, json_data):
        """
        Create a log entry representing:

        `log_entry_creator` has performed `operation` on an instance of `model` belonging
        to `user`. The instance's data is `json_data`.
        """
        self.create(
            creator=log_entry_creator,
            operation=operation,
            model_path=get_model_path(model),
            user=user,
            data=json_data,
        )

    def retrieve_for_user(self, model, user):
        """Return all log entries for this user on this model."""
        return self.filter(user=user, model_path=get_model_path(model))

    def retrieve_for_creator(self, model, creator):
        """Return all log entries logged by this user on this model."""
        return self.filter(creator=creator, model_path=get_model_path(model))


class LogEntry(models.Model):
    """
    A change that has been made to an instance of another model.

    Stores:
    - date_created: The datetime that the change was made.
    - creator: Who made the change.
    - operation: 'Added', 'Removed' or 'Modified'.
    - model_path: The path to the model that's been operated-on.
    - data: JSON data representing the model after the operation, or just before it in
      the case of a 'Removed' operation.
    - user: The user whose model instance it is.
    """
    OPERATION_ADDED = 'added'
    OPERATION_REMOVED = 'removed'
    OPERATION_MODIFIED = 'modified'
    OPERATION_CHOICES = (
        (OPERATION_ADDED, _('Added')),
        (OPERATION_REMOVED, _('Removed')),
        (OPERATION_MODIFIED, _('Modified')),
    )

    date_created = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='log_entries_created',
    )

    operation = models.CharField(choices=OPERATION_CHOICES, max_length=255)
    model_path = models.CharField(max_length=255)
    data = TextPGPPublicKeyField(default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='log_entries',
    )

    objects = LogEntryManager()

    class Meta:
        ordering = ('date_created',)
