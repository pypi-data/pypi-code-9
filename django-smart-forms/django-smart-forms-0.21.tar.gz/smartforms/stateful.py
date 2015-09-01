# coding: utf8
from django import forms
from django.http import QueryDict
from django.middleware.csrf import _get_new_csrf_key


class StatefulForm(forms.Form):
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
        if self.is_bound: # form initialized with post data
            self.initial_from_session = False
            return

        session_data = self.session.get(self.session_key, {})
        if len(session_data):
            for key, value in session_data.items():
                self.data[key] = value

            self.initial_from_session = True
            self.is_bound = True

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        if self.session is None or not hasattr(self.session, '__getitem__'):
            raise ValueError("Please set session parameter")

        super(StatefulForm, self).__init__(*args, **kwargs)
        self._override_data_with_session()

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