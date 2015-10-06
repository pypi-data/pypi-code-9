import json

import factory
from django.contrib.auth.models import User

from model_logging import models


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence('User {}'.format)

    class Meta:
        model = User


class LogEntryFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    creator = factory.SubFactory(UserFactory)
    operation = models.LogEntry.OPERATION_ADDED
    model_path = models.get_model_path(models.LogEntry)
    data = json.dumps({'item': 42})

    class Meta:
        model = models.LogEntry
