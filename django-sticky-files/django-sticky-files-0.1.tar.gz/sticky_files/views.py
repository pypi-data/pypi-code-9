# coding: utf-8

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import File


# TODO: think about login required?
@csrf_exempt
@require_POST
def upload_file(request, form_class):
    form = form_class(request.POST, request.FILES)

    if request.method == "POST":
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            f = File.objects.create(file=uploaded_file)
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
