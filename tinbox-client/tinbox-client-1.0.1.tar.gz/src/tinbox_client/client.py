from functools import wraps
import json
import logging

from .auth import get_oauth_session
from .settings import get_settings

_log = logging.getLogger(__name__)


def with_default_headers(f):

    @wraps(f)
    def wrapper(*args, **kw):
        if 'headers' not in kw:
            kw['headers'] = {
                'content-type': 'application/json',
            }
        return f(*args, **kw)

    return wrapper


class Tinbox:
    def __init__(self):
        self.session = get_oauth_session()
        self.settings = get_settings()

    def get_url(self, *args, **kw):
        return self.settings.get_url(*args, **kw)

    def _get_default_headers(self):
        return {
            'content-type': 'application/json'
        }

    def _get_assignment_path(self, ticket_pk):
        return '/'.join((
            'tickets',
            str(ticket_pk),
            'assignment',
            ''))

    @with_default_headers
    def post(self, path, *args, **kw):
        return self.session.post(self.get_url(path), *args, **kw)

    @with_default_headers
    def put(self, path, *args, **kw):
        return self.session.put(self.get_url(path), *args, **kw)

    def get(self, path, *args, **kw):
        return self.session.get(self.get_url(path), *args, **kw)

    def delete(self, path, *args, **kw):
        return self.session.delete(self.get_url(path), *args, **kw)

    def get_ticket(self, ticket_pk):
        request = self.get('tickets/{}/'.format(ticket_pk))
        return request.json()

    def create_ticket(self, sender_email, subject, body, sender_name=None,
                      context=None, attachments=None):
        data = {'sender_email': sender_email,
                'sender_name': sender_name,
                'subject': subject,
                'body': body,
                'attachments': attachments}

        if context is not None:
            data.update({'pks': context})

        request = self.post('tickets/',
                            data=json.dumps(data))

        return request.json()

    def list_tickets(self, assignee=None, inbox=None, labels=None, pks=True):

        data = {}
        # List function arguments and iterate
        for arg in list_tickets.__code__.co_varnames:
            if arg == 'self':
                continue

            val = locals()[arg]
            if val is not None:
                data[arg] = val
        request = self.get('tickets/', data=data)
        return request.json()

    def delete_ticket(self, ticket_pk):
        return self.delete('tickets/{}/'.format(ticket_pk)).json()

    def get_attachment(self, attachment_pk):
        return self.get('attachments/{}/'.format(
            attachment_pk
        )).json()

    def upload_attachment(self, attachment_pk, attachment_bytes):
        return self.put(
            'attachments/{}/'.format(attachment_pk),
            data=attachment_bytes,
            headers={
                'content-type': 'application/binary'
            }
        ).json()

    def delete_attachment(self, attachment_pk):
        request = self.delete('attachments/{}/'.format(
            attachment_pk
        ))
        return request.json()

    def list_attachments(self, message_pk):
        request = self.get('attachments/',
                           data={
                               'message_pk': message_pk
                           })
        return request.json()

    def get_message(self, message_pk):
        request = self.get('messages/{}/'.format(message_pk))
        return request.json()

    def delete_message(self, message_pk):
        request = self.delete('messages/{}/'.format(message_pk))
        return request.json()

    def list_messages(self, ticket_pk):
        request = self.get('messages/', data={
            'ticket_pk': ticket_pk
        })
        return request.json()

    def create_message(self, thread_id, *args, **kwargs):
        return self.create_ticket(*args, context=thread_id, **kwargs)

    def get_me(self):
        request = self.get('me/')
        return request.json()

    def assign_ticket(self, ticket_pk, assignee_pk):
        path = self._get_assignment_path(ticket_pk)
        request = self.put(path, data=json.dumps({
            'assignee_pk': assignee_pk
        }))
        return request.json()

    def unassign_ticket(self, ticket_pk):
        path = self._get_assignment_path(ticket_pk)
        request = self.delete(path)
        return request.json()

    def get_assignment(self, ticket_pk):
        path = self._get_assignment_path(ticket_pk)
        request = self.get(path)
        return request.json()

    def get_desk(self, helpdesk_pk):
        request = self.get('desks/{}/'.format(helpdesk_pk))
        return request.json()

    def list_desks(self):
        return self.get('desks/').json()

    def get_filter(self, filter_pk):
        return self.get('filters/{}/'.format(filter_pk)).json()

    def list_filters(self):
        return self.get('filters/').json()
