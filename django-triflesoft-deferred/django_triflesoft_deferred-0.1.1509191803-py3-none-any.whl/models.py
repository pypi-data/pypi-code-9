from pickle import loads
from pickle import dumps

from django.db.models import AutoField
from django.db.models import BinaryField
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import Manager
from django.db.models import Model
from django.db.models import TextField

from deferred.helpers import HttpRequest
from deferred.helpers import SendEMail


class TaskManager(Manager):
    def create_generic(self, priority, generic_object):
        task = Task()
        task.type = type(generic_object).__name__
        task.data = dumps(generic_object)
        task.priority = priority
        task.retry_count = 0
        task.is_processed = False
        task.is_succeeded = False
        task.save()

    def create_email(self, priority, message):
        self.create_generic(priority, SendEMail(message))

    def create_http(self, priority, verb, url, parameters=None, headers=None, data=None):
        self.create_generic(priority, HttpRequest(verb, url, parameters, headers, data))


class Task(Model):
    objects = TaskManager()

    id                  = AutoField(                               blank=False, unique=False, primary_key=True)
    created_at          = DateTimeField(                           blank=False, unique=False, auto_now_add=True)
    updated_at          = DateTimeField(                           blank=False, unique=False, auto_now=True)
    type                = CharField(                               blank=False, unique=False, max_length=256)
    data                = BinaryField(                             blank=False, unique=False)
    priority            = IntegerField(                            blank=False, unique=False)
    retry_count         = IntegerField(                            blank=False, unique=False)
    is_processed        = BooleanField(                            blank=False, unique=False, default=False)
    is_succeeded        = BooleanField(                            blank=False, unique=False, default=False)

    def to_object(task):
        return loads(task.data)

    def __str__(self):
        return '{0} - {1}'.format(self.type, self.priority)

    class Meta:
        ordering            = ['-priority']
        index_together      = [('priority', 'type', 'data')]
        unique_together     = []
        verbose_name        = 'Task'
        verbose_name_plural = 'Tasks'


class Failure(Model):
    id                  = AutoField(                               blank=False, unique=False, primary_key=True)
    task                = ForeignKey(Task,                         blank=False, unique=False, null=True)
    created_at          = DateTimeField(                           blank=False, unique=False, auto_now_add=True)
    exception_type      = CharField(                               blank=True,  unique=False, null=True, max_length=256)
    exception_args      = TextField(                               blank=True,  unique=False, null=True)

    def __str__(self):
        return '{0:%Y-%m-%d %H:%M:%S}'.format(self.created_at)

    class Meta:
        ordering            = ['created_at']
        index_together      = []
        unique_together     = []
        verbose_name        = 'Failure'
        verbose_name_plural = 'Failures'
