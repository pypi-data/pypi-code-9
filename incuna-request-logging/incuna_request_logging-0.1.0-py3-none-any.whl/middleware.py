from .models import Log


class LogAuthenticatedRequestMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated():
            Log.objects.from_request(request)
