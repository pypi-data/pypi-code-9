from hashlib import sha512
from os import urandom

from django.conf import settings

from django.db.models import AutoField
from django.db.models import BinaryField
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Model


class Token(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    code                = CharField(                               blank=False, unique=True,  max_length=64)
    user                = ForeignKey(settings.AUTH_USER_MODEL,     blank=False, unique=False)
    path_pattern        = CharField(                               blank=False, unique=False, max_length=256)
    method_pattern      = CharField(                               blank=False, unique=False, max_length=256)
    valid_from          = DateTimeField(                           blank=False, unique=False)
    valid_till          = DateTimeField(                           blank=False, unique=False)
    can_md5             = BooleanField(                            blank=False, unique=False, default=False)
    can_sha1            = BooleanField(                            blank=False, unique=False, default=False)
    can_sha256          = BooleanField(                            blank=False, unique=False, default=False)
    can_sha512          = BooleanField(                            blank=False, unique=False, default=False)
    secret              = BinaryField(                             blank=False, unique=True,  max_length=64)

    def _get_secret_field_names(self):
        return ['secret']

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = sha512(urandom(64)).hexdigest().encode('ascii')

        super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return '{0}/{1}'.format(self.user, self.path_pattern)

    class Meta:
        ordering            = ['user', 'path_pattern', 'method_pattern', 'valid_from']
        index_together      = []
        unique_together     = []
        verbose_name        = 'Token'
        verbose_name_plural = 'Tokens'
