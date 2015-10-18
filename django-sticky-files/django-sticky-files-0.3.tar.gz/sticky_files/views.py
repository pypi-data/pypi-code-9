# coding: utf-8

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.apps import apps


# TODO: think about login required?
@csrf_exempt
@require_POST
def upload_file(request, app, model, form_class):
    form = form_class(request.POST, request.FILES)

    if request.method == "POST":
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            file_model_class = apps.get_model(app, model)
            f = file_model_class.objects.create(file=uploaded_file)
            return JsonResponse({
                'url': f.file.url,
                'name': f.file.name,
                'id': f.pk,
                'filetype': f.filetype,
            })
        else:
            return JsonResponse(
                form.errors,
                status=400,
            )
