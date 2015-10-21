__author__ = 'vinay'
import json
import traceback

from django.conf import settings
from django.http.response import HttpResponseForbidden, HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from .models import Content
from .response import render
from .utils import NAMESPACE_DELIMITER, user_passes_test, can_edit_content


def cms_page_index(request, cms_page=None, url_path=None):
    if not cms_page:
        url_path = url_path or request.path_info

        if not url_path.startswith('/'):
            url_path = u'/{}'.format(url_path)

        if settings.APPEND_SLASH and not url_path.endswith('/'):
            url_path = u'{}/'.format(url_path)

        cms_page = get_object_or_404(Content, url=url_path)

    if can_edit_content(request.user):
        return render(
            template_name=cms_page.template,
            cms_context=cms_page.auth_data,
            request=request,
            template_context={'view': 'author',
                              'cms_data': json.dumps(cms_page.auth_data),
                              'id': cms_page.id,
                              'namespace_delimiter': json.dumps(NAMESPACE_DELIMITER)})

    if cms_page.is_public:
        return HttpResponse(cms_page.html)

    raise Http404("page not found")


@require_POST
@csrf_protect
@user_passes_test()
def save(request, save_type):
    if not request.is_ajax():
        return HttpResponseForbidden()

    post_data = request.POST
    if any(_ not in post_data for _ in ('auth_data', 'cms_page_id')) or save_type not in ('draft', 'publish'):
        return JsonResponse({'success': False}, status=400)

    cms_page = get_object_or_404(Content, id=post_data['cms_page_id'])

    try:
        content = json.loads(post_data['auth_data'])
    except:
        return JsonResponse({'success': False, 'message': 'Invalid JSON object'}, status=400)
    else:
        cms_page.auth_data.update(content)
        try:
            render(cms_page.template, cms_context=cms_page.auth_data)
        except Exception as e:
            return JsonResponse({'success': False,
                                 'message': 'Unable to parse the new content.\n'
                                 'Please check the console for issues.',
                                 'exception': unicode(e),
                                 'traceback': traceback.format_exc()})
        else:
            if save_type == 'draft':
                cms_page.save()
            else:
                cms_page.publish_cms_content()
            return JsonResponse({'success': True})
