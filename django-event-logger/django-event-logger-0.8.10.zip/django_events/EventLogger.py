from django.contrib.auth import get_user_model
from .models import Event


def log_event(action, response, request, additional=None, invoker=None):
    auth_user = get_user_model()

    self.action = action
    self.response = response
    self.additional = additional

    self.request = request
    if request.user is None:
        self.invoker = auth_user.objects.get(username=invoker)
    else:
        self.invoker = request.user

    # Let's grab the current IP of the user.
    x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = self.request.META.get('REMOTE_ADDR')

    Event(invoker=self.invoker, action=self.action, response=self.response, ip=ip,
          additional=self.additional).save()


def get_logs(account=None):
    if account:
        # We want logs for a specific account.
        return Event.objects.filter(invoker=account)
    # We want logs in general.
    return Event.objects.all()
