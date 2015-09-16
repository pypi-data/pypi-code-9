from copy import deepcopy

from django.test import TestCase, RequestFactory

from .forms import TestStatefulForm


class StatefulFormTestCase(TestCase):
    def test_init(self):
        """
        Initialize without session object raises error.

        Initialize with empty session > work like a normal form.
        """
        self.assertRaises(ValueError, lambda: TestStatefulForm())

        ### Stateful form without session data works like a 'normal' form
        session = {}
        form = TestStatefulForm(session=session)

        self.assertEqual(form.is_bound, False)
        self.assertEqual(form.is_valid(), False)

    def test_init_with_session(self):
        """
        Stateful form with session data (no posted data) is valid
        """
        session = dict()
        session['TestStatefulForm'] = {}
        session['TestStatefulForm']['value1'] = 'test value'
        session['TestStatefulForm']['value2'] = '2'
        session_copy = deepcopy(session)

        form = TestStatefulForm(session=session)
        self.assertEqual(form.is_valid(), True) # The form is valid (because we bound the form with the session data)
        self.assertEqual(form.is_bound, True)
        self.assertEqual(session_copy['TestStatefulForm'], form.cleaned_data)

    def test_session_update(self):
        """
        Stateful form override the session data after validation
        """
        post = {'value1': 'posted data', 'value2': '1'}
        factory = RequestFactory()
        request = factory.post('/', post)

        session = dict()
        session['TestStatefulForm'] = {'value1': 'asdf'}

        form = TestStatefulForm(request.POST, session=session)

        self.assertEqual(session['TestStatefulForm'], {'value1': 'asdf'})
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(session['TestStatefulForm'], {'value1': 'posted data', 'value2': '1'})

    def test_session_update_ignore(self):
        """
        Stateful doesn't override the session data, if the posted data isn't valid
        """
        post = {'value1':'posted data', 'value2':'1'}
        factory = RequestFactory()
        request = factory.post('/', post)

        session = dict()
        session['TestStatefulForm'] = {'value1': 'asdf'}

        form = TestStatefulForm({'value1': 'posted data', 'value2': '3'}, session=session)

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(session['TestStatefulForm'], {'value1': 'asdf'})

    def test_init_outdated_session(self):
        """
        If the session data isn't valid (outdated), then create empty form (not bounded)
        """
        session = dict()
        session['TestStatefulForm'] = {'value1': 'wrong session data', 'value2': '3'}

        form = TestStatefulForm(session=session)
        self.assertEquals(form.is_valid(), False)
        self.assertEqual(form.is_bound, False)
        self.assertEqual(form.data, {})
        self.assertEqual(session['TestStatefulForm'], None)

### TODO test form prefix