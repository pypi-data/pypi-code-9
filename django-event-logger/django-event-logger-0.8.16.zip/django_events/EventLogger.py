from django.contrib.auth import get_user_model
from .models import Event


def log_event(action, response, request, additional=None, invoker=None):
    auth_user = get_user_model()

    action = action
    response = response
    additional = additional

    request = request
    if request.user is None:
        if invoker is None:
            raise Exception('No invoker was specified, and no user is detected!')
        invoker = auth_user.objects.get(username=invoker)
    else:
        invoker = request.user

    # Let's grab the current IP of the user.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    Event(account=invoker, action=action, response=response, ip=ip,
          additional=additional).save()


def get_logs(account=None):
    if account:
        # We want logs for a specific account.
        return Event.objects.filter(account=account)
    # We want logs in general.
    return Event.objects.all()
