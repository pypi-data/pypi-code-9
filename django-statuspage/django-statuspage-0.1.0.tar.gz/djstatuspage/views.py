from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from djstatuspage.models import Status


class BaseStatusView(View):
    response_class = JsonResponse

    def get_context_data(self, **kwargs):
        return kwargs

    def render_to_response(self, context):
        return self.response_class(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class DefaultStatusPage(BaseStatusView):
    def get_database_status(self):
        try:
            (status, _) = Status.objects.get_or_create(pk=1)
            if status.id == 1:
                return "ok"
        except:
            pass

        return "error"

    def get_context_data(self, **kwargs):
        tasks = getattr(settings, "STATUSPAGE_TASKS", None)
        if not tasks:
            tasks = {}

        if getattr(settings, "STATUSPAGE_TRY_DATABASE", True):
            tasks["database"] = self.get_database_status

        for key, task in tasks.items():
            if not callable(task):
                continue
            kwargs[key] = task()

        return kwargs