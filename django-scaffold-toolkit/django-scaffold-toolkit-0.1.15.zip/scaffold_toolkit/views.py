#coding=utf-8
import json
import datetime

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, FormView
from scaffold_toolkit.tagging.models import Tag
import shortuuid


class AjaxFormView(JSONResponseMixin, AjaxResponseMixin, FormView):
    def form_invalid(self, form):
        """
        表单校验错误
        :param form:
         :type form: django.forms.form
        :return:
        """
        return self.render_json_response({'success': False,
                                          'msg': json.loads(form.errors.as_json())})


class AjaxView(JSONResponseMixin, AjaxResponseMixin, View):
    pass


IMAGE_EXT_NAMES = getattr(settings, 'KINDEDITOR_IMAGE_EXT', ('.jpg', '.png', '.gif', '.bmp'))
FLASH_EXT_NAMES = getattr(settings, 'KINDEDITOR_FLASH_EXT', ('.swf'))
MAX_SIZE = getattr(settings, 'KINDEDITOR_UPLOAD_SIZE', 5) * 1024 * 1024  # 5M
MAX_SIZE_M = MAX_SIZE / 1024 / 1024


@csrf_exempt
@require_http_methods(['POST'])
def kindeditor_upload_file(request):
    uploaded_file = request.FILES['imgFile']

    if not uploaded_file.name:
        return HttpResponse(json.dumps({'error': 1, 'message': u'请选择要上传的文件'}))

    ext = os.path.splitext(uploaded_file.name)[1]
    upload_dir = request.GET['dir']
    allowed_exts = None
    if upload_dir == 'image':
        allowed_exts = IMAGE_EXT_NAMES
    elif upload_dir == 'flash':
        allowed_exts = FLASH_EXT_NAMES
    elif upload_dir == 'media':
        pass
    if allowed_exts is not None and ext not in allowed_exts:
        return HttpResponse(json.dumps({'error': 1, 'message': u'不允许的文件格式'}))

    if uploaded_file.size > MAX_SIZE:
        return HttpResponse(json.dumps(
            {'error': 1, 'message': u'上传的文件大小不能超过%sMB' % MAX_SIZE_M}
        ))

    upload_to = os.path.join(settings.MEDIA_ROOT, datetime.date.today().strftime('upload%Y'),
                             datetime.date.today().strftime("%m%d"))

    if not os.path.exists(upload_to):
        os.makedirs(upload_to)

    file_name = shortuuid.uuid() + ext
    with open(os.path.join(upload_to, file_name), 'wb+') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    url_name = "{}{}/{}/{}".format(settings.MEDIA_URL,
                                   datetime.date.today().strftime('upload%Y'), datetime.date.today().strftime("%m%d"),
                                   file_name)
    return HttpResponse(json.dumps(
        {'error': 0, 'url': url_name}
    ))


MAX_RESULT = getattr(settings, 'MAX_RESULT', 10)


def tag_suggestion(request):
    """
    tag建议
    @param request:
    @return:
    """
    term = request.GET.get('term')

    tags = [{'id': tag.name, 'text': tag.name}
            for tag in Tag.objects.filter(name__icontains=term)[:MAX_RESULT]]
    return JsonResponse(tags, safe=False)
