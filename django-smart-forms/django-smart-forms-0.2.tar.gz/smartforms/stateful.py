# coding: utf8
from django import forms
from django.http import QueryDict
from django.middleware.csrf import _get_new_csrf_key


class StatefulForm(forms.Form):
    """
        Stateful form persist it's own state between to request in the session.
        It's only persist the DATA, not the FILES.
    """
    def __init__(self, *args, **kwargs):
        # Try to load initials data from the session.
        # At the initialization process store the datasource:
        #         1. If the form is posted, the the datasource is POST (post object)
        #         2. If there isn't any post object, then the data filled from session.
        self.session = kwargs.pop('session', None)
        self.prefix = kwargs.get('prefix', '')
        self.initial_from_session = False
        if self.session is None or not hasattr(self.session, '__getitem__'):
            raise ValueError("Please set session parameter")
        if not len(args) or args[0] is None: ## GET
            #Load data from session
            session_data = self.session.get(self.session_key, {})
            if len(session_data):
                q = QueryDict(None, mutable=True)
                session_data['csrfmiddlewaretoken'] = [_get_new_csrf_key()]
                for key, value in session_data.items():
                    if not isinstance(value, (list, tuple)):
                        value = [value]
                    q.setlist(key, value)
                args = (q,) + args[1:]
                self.initial_from_session = True
        super(StatefulForm, self).__init__(*args, **kwargs)

    @property
    def session_key(self):
        return "{}{}".format(self.prefix or '', self.__class__.__name__)

    def full_clean(self):
        super(StatefulForm, self).full_clean()
        # If the form data is from the session
        if self.initial_from_session:
            # If the form isn't valid, then remove the session data (it's outdated)
            if not hasattr(self, 'cleaned_data'):
                self.data = {}
                self.is_bound = False
                self.session[self.session_key] = None
        else:
            if not self._errors and self.is_bound:
                post = {}
                for key, values in self.data.lists():
                    if key not in self.fields:
                        continue
                    post[key] = values
                self.session[self.session_key] = post