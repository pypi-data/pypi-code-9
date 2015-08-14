from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode
from django.template import Context
from django.core import mail


def _get_node(template, name, block_lookups={}):
    """
    Get a named node from a template.
    Returns `None` if a node with the given name does not exist.

    taken from https://github.com/bradwhittington/django-templated-email/blob/master/templated_email/utils.py
    """
    context = Context()
    context.template = template

    for node in template:
        if isinstance(node, BlockNode) and node.name == name:
            for i in range(len(node.nodelist)):
                n = node.nodelist[i]
                if isinstance(n, BlockNode) and n.name in block_lookups:
                    node.nodelist[i] = block_lookups[n.name]
            return node
        elif isinstance(node, ExtendsNode):
            lookups = dict([(n.name, n) for n in node.nodelist if isinstance(n, BlockNode)])
            lookups.update(block_lookups)
            return _get_node(node.get_parent(context), name, lookups)
    return None


class EmailMessage(mail.EmailMultiAlternatives):
    """Extends standard EmailMessage class with ability to use templates"""

    def __init__(self, template_name, context, *args, **kwargs):
        self._subject = None
        self._body = None
        self._html = None
        # This causes template loading.
        self.template_name = template_name
        # Save context to process on send().
        self.context = context
        super(EmailMessage, self).__init__(*args, **kwargs)
        # It's not set by default, but we may ommit the html content.
        self.alternatives = []

    @property
    def template_name(self):
        return self._template_name

    @template_name.setter
    def template_name(self, value):
        self._template_name = value
        # Load the template.
        self.template = get_template(self._template_name)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):

        if hasattr(value, 'template'):
            value = value.template

        self._template = value
        self._subject = _get_node(value, 'subject')
        self._body = _get_node(value, 'body')
        self._html = _get_node(value, 'html')

    def send(self, *args, **kwargs):
        """Render email with the current context and send it"""
        # Prepare context
        context = Context(self.context)
        context.template = self._template

        # Assume the subject may be set manually.
        if self._subject is not None:
            self.subject = self._subject.render(context).strip('\n\r')
        # Same for body.
        if self._body is not None:
            self.body = self._body.render(context).strip('\n\r')
        # The html block is optional, and it also may be set manually.
        if self._html is not None:
            html = self._html.render(context).strip('\n\r')
            if html:
                if not self.body:
                    # This is html only message.
                    self.body = html
                    self.content_subtype = 'html'
                else:
                    # Add alternative content.
                    self.attach_alternative(html, 'text/html')

        return super(EmailMessage, self).send(*args, **kwargs)

    def __getstate__(self):
        """
        Exclude BlockNode and Template objects from pickling, b/c they can't
        be pickled.
        """
        return dict((k, v) for k, v in self.__dict__.iteritems()
                    if not k in ('_body', '_html', '_subject', '_template'))

    def __setstate__(self, state):
        """
        Use the template_name setter after unpickling so the orignal values of
        _body, _html, _subject and _template will be restored.
        """
        self.__dict__ = state
        self.template_name = self._template_name


def send_mail(template_name, context, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, bcc=None, attachment=None, attachment_info=None):
    """
    Easy wrapper for sending a single message to a recipient list using
    django template system.
    All members of the recipient list will see the other recipients in
    the 'To' field.

    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.
    """

    connection = connection or mail.get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)

    email = EmailMessage(template_name, context, None, None, from_email,
        recipient_list, connection=connection, bcc=bcc)

    if attachment:
        if attachment_info:
            email.attach(attachment_info['filename'],
            attachment_info['content'], attachment_info['mimetype'])
        else:
            email.attach_file(attachment)

    return email.send()