# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.vary import vary_on_cookie

from pybb import defaults
from pybb.views import PaginatorMixin

from private_messages.forms import MessageForm
from private_messages.models import PrivateMessage, MessageHandler


class InboxView(PaginatorMixin, generic.ListView):
    paginate_by = defaults.PYBB_TOPIC_PAGE_SIZE
    context_object_name = 'message_list'
    template_name = 'pybb/private_messages/inbox.html'

    def get_queryset(self):
        return self.request.user.inbox.all().select_related()

    @method_decorator(login_required)
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(InboxView, self).dispatch(request, *args, **kwargs)


class MessageView(generic.DetailView):

    queryset = PrivateMessage.objects.all()
    template_name = 'pybb/private_messages/message.html'
    context_object_name = 'message'
    http_method_names = ['get', ]

    @method_decorator(login_required)
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        message = super(MessageView, self).get_object(queryset)
        if message not in self.request.user.inbox.all() and message.sender != self.request.user:
            raise PermissionDenied
        try:
            handler = MessageHandler.objects.get(message=message, receiver=self.request.user)
            handler.read = True
            handler.save()
        except MessageHandler.DoesNotExist:
            pass
        return message


class SendMessageView(generic.CreateView):

    template_name = 'pybb/private_messages/new.html'
    form_class = MessageForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SendMessageView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'receivers': self.request.GET.getlist('to')}

    def form_valid(self, form):
        message = PrivateMessage(
            sender=self.request.user,
            sender_ip=self.request.META.get('REMOTE_ADDR', ''),
            subject=form.cleaned_data['subject'],
            body=form.cleaned_data['body'],
            )
        message.save()
        for receiver in form.cleaned_data['receivers']:
            MessageHandler(message=message, receiver=receiver).save()
        return HttpResponseRedirect(message.get_absolute_url())
