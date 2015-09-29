# -*- coding: utf-8 -*-

def unread_messages(request):
    context = {}
    if request.user.is_authenticated():
        context['unread_msgs'] = request.user.recd_messages.filter(messagehandler__read=False).count()
    return context
