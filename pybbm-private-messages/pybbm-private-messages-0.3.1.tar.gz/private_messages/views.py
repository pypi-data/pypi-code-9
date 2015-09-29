# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.vary import vary_on_cookie
from django_select2 import Select2View
from pybb import defaults
from pybb.compat import get_username_field
from pybb.util import get_markup_engine, get_pybb_profile_model
from pybb.views import PaginatorMixin

from private_messages.forms import MessageForm
from private_messages.models import PrivateMessage, MessageHandler, MessageThread

MarkupEngine = get_markup_engine()


class InboxView(PaginatorMixin, generic.ListView):
    paginate_by = defaults.PYBB_TOPIC_PAGE_SIZE
    context_object_name = 'message_list'
    template_name = 'pybb/private_messages/inbox.html'

    def get_queryset(self):
        return self.group_into_threads(self.get_messages())

    def get_messages(self):
        return PrivateMessage.objects.filter(messagehandler__receiver=self.request.user, messagehandler__deleted=False)

    def group_into_threads(self, messages):
        """
        Get thread for each message and remove dupes. The reason for creating instances of MessageThread rather than
        using message.thread is that the latter runs a useless query for thread.id WHERE thread.id = %s.
        :param messages: list or queryset of PrivateMessage instances
        :return: list of MessageThread instances.
        """
        inbox = OrderedDict((MessageThread(id=message.thread_id), None) for message in messages)
        return list(inbox.keys())

    @method_decorator(login_required)
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(InboxView, self).dispatch(request, *args, **kwargs)


class OutboxView(InboxView):
    def get_messages(self):
        return PrivateMessage.objects.filter(sender=self.request.user, sender_deleted=False)

    def get_context_data(self, **kwargs):
        ctx = super(OutboxView, self).get_context_data(**kwargs)
        ctx['outbox'] = True
        return ctx


class MessageView(generic.DetailView):
    queryset = PrivateMessage.objects.all()
    template_name = 'pybb/private_messages/message.html'
    context_object_name = 'thread'
    http_method_names = ['get', ]

    @method_decorator(login_required)
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        message = super(MessageView, self).get_object(queryset)
        if message.sender != self.request.user:
            try:
                handler = MessageHandler.objects.get(message=message, receiver=self.request.user, deleted=False)
            except MessageHandler.DoesNotExist:
                raise Http404
            handler.read = True
            handler.save()
            deleted_filter = Q(messagehandler__receiver=self.request.user, messagehandler__deleted=False) | \
                             Q(sender=self.request.user, sender_deleted=False)
        else:
            deleted_filter = Q(sender_deleted=False) |\
                             Q(messagehandler__receiver=message.sender, messagehandler__deleted=False)
        thread = [message]
        parent = message.get_parent()
        if parent is not None:
            thread.insert(0, parent)
        thread.extend(message.get_children().filter(deleted_filter))
        return thread

    def get_context_data(self, **kwargs):
        ctx = super(MessageView, self).get_context_data(**kwargs)
        ctx['this_message'] = super(MessageView, self).get_object()
        return ctx


class SendMessageView(generic.CreateView):
    template_name = 'pybb/private_messages/new.html'
    form_class = MessageForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SendMessageView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        receivers = self.request.GET.getlist('to')
        parent_pk = self.request.GET.get('reply')
        reply_all = self.request.GET.get('all')
        if receivers:
            return {'receivers': receivers}
        if parent_pk:
            parent = get_object_or_404(PrivateMessage, pk=parent_pk)
            if self.request.user not in parent.receivers.all() and self.request.user != parent.sender:
                raise PermissionDenied
            body = MarkupEngine.quote(parent.body)
            initial = {
                'subject': reply_subject(parent.subject),
                'body': body,
                'receivers': [parent.sender],
                'parent': parent_pk
            }
            if reply_all == 'true':
                initial['receivers'] += parent.receivers.exclude(self.request.user)
            return initial

    def form_valid(self, form):
        parent_pk = form.cleaned_data['parent']
        if not parent_pk:
            thread = MessageThread.objects.create()
        else:
            try:
                parent = PrivateMessage.objects.get(pk=parent_pk)
            except PrivateMessage.DoesNotExist:
                raise Http404
            thread = parent.thread
        self.object = PrivateMessage.objects.create(
            thread=thread,
            sender=self.request.user,
            sender_ip=self.request.META.get('REMOTE_ADDR', ''),
            subject=form.cleaned_data['subject'],
            body=form.cleaned_data['body'],
        )
        receivers = form.cleaned_data['receivers'].exclude(pk=self.object.sender.pk)
        for receiver in receivers:
            MessageHandler.objects.create(message=self.object, receiver=receiver)

        return HttpResponseRedirect(self.get_success_url())


class DeleteMessageView(generic.DeleteView):
    queryset = PrivateMessage.objects.all()
    success_url = reverse_lazy('private_messages:inbox')
    template_name = 'pybb/private_messages/confirm_delete.html'
    context_object_name = 'message'

    @method_decorator(login_required)
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteMessageView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(sender=user) | Q(receivers=user))

    def delete(self, request, *args, **kwargs):
        message = self.get_object(self.get_queryset())
        if message.sender == self.request.user:
            message.sender_deleted = True
            message.save()
        else:
            handler = MessageHandler.objects.get(message=message, receiver=self.request.user)
            handler.deleted = True
            handler.save()
        return HttpResponseRedirect(self.success_url)


def reply_subject(string):
    if string.startswith('RE:'):
        return string
    return 'RE: ' + string


class ReceiversSelect2View(Select2View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(ReceiversSelect2View, self).get(request, *args, **kwargs)

    def get_results(self, request, term, page, context):
        username_field = get_username_field()
        lookup = {'user__{}__icontains'.format(username_field): term}
        results = get_pybb_profile_model().objects.filter(**lookup)\
            .values_list('user__id', 'user__{}'.format(username_field))
        return ('nil', False, results)
