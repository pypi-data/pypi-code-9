from django.conf import settings
from django.db import models


class Event(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL)  # The account an action was triggered on.
    action = models.CharField(max_length=255)  # The action the user tried to preform.
    response = models.IntegerField()  # The response code returned by the server.
    ip = models.GenericIPAddressField()  # The IP of the invoker.
    time = models.DateTimeField(auto_now_add=True)
    additional = models.CharField(max_length=255, default='N/A')  # Additional information (optional).

    def __str__(self):
        return self.action
