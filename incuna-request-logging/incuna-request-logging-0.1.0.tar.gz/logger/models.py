from django.db import models
from django.utils import timezone


class LogManager(models.Manager):
    def from_request(self, request):
        user = request.user
        return self.create(
            user_pk=user.pk,
            registration_date=user.date_joined,
            url=request.build_absolute_uri(),
            request_method=request.method,
        )


class Log(models.Model):
    user_pk = models.PositiveIntegerField()
    registration_date = models.DateTimeField()
    timestamp = models.DateTimeField(default=timezone.now)
    url = models.TextField()
    request_method = models.CharField(max_length=255)

    objects = LogManager()
