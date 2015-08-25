# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.core.urlresolvers import reverse
import json
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
import models, forms
import logging
logger = logging.getLogger("favman")

def _user_message(request, msg_id):
    t = get_template('favman/user_messages/_{0}.html'.format(msg_id))
    return t.render(RequestContext(request, {}))

#@login_required
def toggle_favorite(request):
    try:
        if not request.user.is_authenticated():
            data = {'success': False, 'message': _user_message(request, "user_not_logged"), 'logged': False}
        else:
            if request.method == "POST":
                form = forms.UpdateFavoriteForm(request.POST)
                
                if form.is_valid():
                    object_id = form.cleaned_data["object_id"]
                    content_type = form.cleaned_data["content_type"]
                    
                    favorite, is_new = models.Favorite.objects.get_or_create(
                        user = request.user,
                        content_type = content_type,
                        object_id = object_id
                    )
                    
                    if not favorite.content_object:
                        favorite.delete()
                        raise Exception(_(u'Invalid object'))
                
                    label = getattr(favorite.content_object, 'name', unicode(favorite.content_object))
                    if is_new:
                        data = {
                            'success': True,
                            'status': 'in-fav',
                            'logged': True,
                        }
                    else:
                        favorite.delete()
                        data = {
                            'success': True,
                            'status': 'out-fav',
                            'logged': True,
                        }
                else:
                    raise Exception(u"{0}".format(form.errors))
            else:
                raise Exception(u"POST expected")
    except Exception:
        data = {'success': False, 'message': _(u'An error occured'), 'logged': True}
        logger.exception("update_favorite")
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def list_favorites(request):
    
    content_types = ContentType.objects.filter(favorite__user=request.user).distinct()
    
    favs_by_type = []
    for ct in content_types:
        favs_by_type.append(
            (ct, [
                x.content_object for x in models.Favorite.objects.filter(user=request.user, content_type=ct)
            ])
        )
        
    context = {
        'favs_by_type': favs_by_type,
    }
    
    return render_to_response(
        'favman/favorites_list.html',
        context,
        context_instance=RequestContext(request)
    )
