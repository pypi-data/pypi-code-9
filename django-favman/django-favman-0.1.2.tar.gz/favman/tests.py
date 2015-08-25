# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission, AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template import Template, Context
import json
from model_mommy import mommy
from models import Favorite

class BaseTestCase(TestCase):
    
    def _log_in(self):
        user = User.objects.create_user('toto', 'toto@toto.fr', 'toto')
        user.save()
        if self.client.login(username='toto', password='toto'):
            return user
        return None
    
class UpdateFavoriteTestCase(BaseTestCase):
    
    def _template_content(self):
        return """
        {% load favman_tags %}
        {% fav_media %}
        <ul class="users">
        {% for u in users %}
            <li>{{ u.username }}{% fav_item u %}</li>
        {% endfor %}
        </ul>
        """
        
    def test_render_template(self):
        user = self._log_in()
        for i in xrange(5):
            mommy.make_one(User)
        
        
        template = Template(self._template_content())
        
        class DummyRequest(object): pass
        dummy_request = DummyRequest()
        setattr(dummy_request, 'user', user)
        context = {
            'users': User.objects.all(),
            'request': dummy_request,
        }
        
        html = template.render(Context(context))
        
    def test_render_template_not_logged(self):
        for i in xrange(5):
            mommy.make_one(User)
        
        template = Template(self._template_content())
        
        class DummyRequest(object): pass
        dummy_request = DummyRequest()
        setattr(dummy_request, 'user', AnonymousUser())
        context = {
            'users': User.objects.all(),
            'request': dummy_request,
        }
        
        html = template.render(Context(context))
        
    def test_post_not_logged(self):
        user = mommy.make_one(User)
        data = {
            'content_type': ContentType.objects.get_for_model(User).id,
            'object_id': user.id, 
        }
        response = self.client.post(reverse('favman_toggle'), data)
        self.assertEqual(200, response.status_code)
        resp_data = json.loads(response.content)
        self.assertEqual(resp_data['success'], False)
        self.assertEqual(resp_data['logged'], False)
        self.assertEqual(0, Favorite.objects.count())
        
        
    def test_post_add(self):
        logged_user = self._log_in()
        faved_user = mommy.make_one(User)
        
        data = {
            'content_type': ContentType.objects.get_for_model(User).id,
            'object_id': faved_user.id, 
        }
        
        response = self.client.post(reverse('favman_toggle'), data)
        self.assertEqual(200, response.status_code)
        resp_data = json.loads(response.content)
        self.assertEqual(True, resp_data['success'])
        self.assertEqual('in-fav', resp_data['status'])
        self.assertEqual(1, Favorite.objects.count())
        
        fav = Favorite.objects.all()[0]
        self.assertEqual(fav.content_object, faved_user)
        self.assertEqual(fav.user, logged_user)
        
    def test_post_remove(self):
        logged_user = self._log_in()
        faved_user = mommy.make_one(User)
        
        user_ct = ContentType.objects.get_for_model(User)
        Favorite.objects.create(user=logged_user, object_id=faved_user.id,
            content_type=user_ct)
        self.assertEqual(1, Favorite.objects.count())
        
        data = {
            'content_type': user_ct.id,
            'object_id': faved_user.id, 
        }
        response = self.client.post(reverse('favman_toggle'), data)
        self.assertEqual(200, response.status_code)
        resp_data = json.loads(response.content)
        self.assertEqual(True, resp_data['success'])
        self.assertEqual('out-fav', resp_data['status'])
        self.assertEqual(0, Favorite.objects.count())
        
        
    def test_post_wrong_id(self):
        logged_user = self._log_in()
        
        user_ct = ContentType.objects.get_for_model(User)
        
        data = {
            'content_type': user_ct.id,
            'object_id': 1111, 
        }
        response = self.client.post(reverse('favman_toggle'), data)
        self.assertEqual(200, response.status_code)
        resp_data = json.loads(response.content)
        self.assertEqual(False, resp_data['success'])
        
    def test_post_wrong_ct(self):
        logged_user = self._log_in()
        faved_user = mommy.make_one(User)
        
        user_ct = ContentType.objects.get_for_model(User)
        
        data = {
            'content_type': 55555,
            'object_id': faved_user.id, 
        }
        response = self.client.post(reverse('favman_toggle'), data)
        self.assertEqual(200, response.status_code)
        resp_data = json.loads(response.content)
        self.assertEqual(False, resp_data['success'])
        
        
class ListFavoritesTestCase(BaseTestCase):
    
    def test_not_logged(self):
        response = self.client.get(reverse('favman_list'))
        self.assertEqual(302, response.status_code)
        self.assertTrue(response['Location'].find('login')>0)
        
    def test_empty_list(self):
        self._log_in()
        response = self.client.get(reverse('favman_list'))
        self.assertEqual(200, response.status_code)
        
    def test_list(self):
        logged_user = self._log_in()
        faved_users = [mommy.make_one(User, username='user-{0}'.format(i)) for i in xrange(5)]
        not_faved_users = [mommy.make_one(User, username='NOT-{0}'.format(i)) for i in xrange(5)]
        
        user_ct = ContentType.objects.get_for_model(User)
        for u in faved_users:
            Favorite.objects.create(user=logged_user, content_type=user_ct, object_id=u.id)
        
        response = self.client.get(reverse('favman_list'))
        self.assertEqual(200, response.status_code)
        for u in faved_users:
            self.assertContains(response, u)
        for u in not_faved_users:
            self.assertNotContains(response, u)
            
    def test_someone_else_list(self):
        logged_user = self._log_in()
        other_user = mommy.make_one(User)
        faved_users = [mommy.make_one(User, username='user-{0}'.format(i)) for i in xrange(5)]
        not_my_faved_users = [mommy.make_one(User, username='OTHER-{0}'.format(i)) for i in xrange(5)]
        
        user_ct = ContentType.objects.get_for_model(User)
        
        for u in faved_users:
            Favorite.objects.create(user=logged_user, content_type=user_ct, object_id=u.id)
        
        for u in not_my_faved_users:
            Favorite.objects.create(user=other_user, content_type=user_ct, object_id=u.id)
        
        response = self.client.get(reverse('favman_list'))
        self.assertEqual(200, response.status_code)
        
        for u in faved_users:
            self.assertContains(response, u)
        for u in not_my_faved_users:
            self.assertNotContains(response, u)
            
    def test_list_different_cts(self):
        logged_user = self._log_in()
        faved_users = [mommy.make_one(User, username='user-{0}'.format(i)) for i in xrange(5)]
        faved_groups = [mommy.make_one(Group, name='group-{0}'.format(i)) for i in xrange(5)]
        
        user_ct = ContentType.objects.get_for_model(User)
        group_ct = ContentType.objects.get_for_model(Group)
        
        for u in faved_users:
            Favorite.objects.create(user=logged_user, content_type=user_ct, object_id=u.id)
        
        for g in faved_groups:
            Favorite.objects.create(user=logged_user, content_type=group_ct, object_id=g.id)
        
        response = self.client.get(reverse('favman_list'))
        self.assertEqual(200, response.status_code)
        for u in faved_users:
            self.assertContains(response, u)
        for u in faved_groups:
            self.assertContains(response, u)
    