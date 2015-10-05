# coding=utf-8
import json
import datetime

from braces.views import AjaxResponseMixin, JSONResponseMixin, PermissionRequiredMixin, LoginRequiredMixin
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View, FormView
from scaffold_toolkit.utilities.misc import get_form_error_message
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
                                          'msg': get_form_error_message(form)})


class AjaxView(JSONResponseMixin, AjaxResponseMixin, View):
    pass


class PermissionRequiredAjaxView(PermissionRequiredMixin, AjaxView):
    """
    有权限要求的AjaxView
    """

    def no_permissions_fail(self, request=None):
        return self.render_json_response({'success': False, 'msg': u'没有权限'})


class LoginRequiredAjaxView(LoginRequiredMixin, AjaxView):
    """
    有登录要求的AjaxView
    """

    def no_permissions_fail(self, request=None):
        return self.render_json_response({'success': False, 'msg': u'没有权限'})


IMAGE_EXT_NAMES = getattr(settings, 'KINDEDITOR_IMAGE_EXT', ('.jpg', '.png', '.gif', '.bmp'))
FLASH_EXT_NAMES = getattr(settings, 'KINDEDITOR_FLASH_EXT', ('.swf'))
MAX_SIZE = getattr(settings, 'KINDEDITOR_UPLOAD_SIZE', 5) * 1024 * 1024  # 5M
MAX_SIZE_M = MAX_SIZE / 1024 / 1024

storage = default_storage


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

    upload_to = os.path.join(datetime.date.today().strftime('kindeditor/upload%Y'),
                             datetime.date.today().strftime("%m%d"))

    if not os.path.exists(upload_to):
        os.makedirs(upload_to)

    file_name = shortuuid.uuid() + ext

    final_name = storage.save(os.path.join(upload_to, file_name), uploaded_file)

    url_name = "{}{}".format(settings.MEDIA_URL, final_name)
    return HttpResponse(json.dumps(
        {'error': 0, 'url': url_name}
    ))
