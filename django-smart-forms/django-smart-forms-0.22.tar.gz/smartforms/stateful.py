# coding: utf8
from django import forms
from django.http import QueryDict
from django.middleware.csrf import _get_new_csrf_key


class StatefulMixin(object):
    """
        Stateful form persist it's own state between to request in the session.
        It's only persist the DATA, not the FILES.
    """
    def _override_data_with_session(self):
        """
        Override form.data values with session data if the method
        """
        # Try to load initials data from the session.
        # At the initialization process store the datasource:
        #         1. If the form is posted, the the datasource is POST (post object)
        #         2. If there isn't any post object, then the data filled from session.
        self.initial_from_session = False
        if self.is_bound:  # form initialized with post data
            return

        session_data = self.session.get(self.session_key, {})
        if len(session_data):
            for key, value in session_data.items():
                self.data[key] = value

            self.initial_from_session = True
            self.is_bound = True

    @property
    def session_key(self):
        return "{}{}".format(getattr(self, 'prefix', None) or '', self.__class__.__name__)

    @property
    def session_dict(self):
        post = {}
        for key, values in self.data.items():
            if key not in self.fields:
                continue
            post[key] = values

        return post

    def handle_session_after_validation(self, is_valid):
        if self.initial_from_session:
            if not is_valid:
                self.data = {}
                self.is_bound = False
                self.session[self.session_key] = None
        else:
            if is_valid:
                self.session[self.session_key] = self.session_dict


class StatefulForm(forms.Form, StatefulMixin):
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        if self.session is None or not hasattr(self.session, '__getitem__'):
            raise ValueError("Please set session parameter")

        super(StatefulForm, self).__init__(*args, **kwargs)
        self._override_data_with_session()

    def is_valid(self):
        valid = super().is_valid()
        self.handle_session_after_validation(valid)
        return valid
