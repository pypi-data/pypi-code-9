from datetime import datetime

from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase, Client, override_settings

from molo.commenting.models import MoloComment


urlpatterns = patterns(
    '',
    url(r'^commenting/', include('molo.commenting.urls')),
)


@override_settings(ROOT_URLCONF='molo.commenting.tests.test_views')
class ViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'test', 'test@example.org', 'test')
        self.content_type = ContentType.objects.get_for_model(self.user)
        self.client = Client()
        self.client.login(username='test', password='test')

    def mk_comment(self, comment):
        return MoloComment.objects.create(
            content_type=self.content_type,
            object_pk=self.user.pk,
            content_object=self.user,
            site=Site.objects.get_current(),
            user=self.user,
            comment=comment,
            submit_date=datetime.now())

    def test_reporting(self):
        comment = self.mk_comment('the comment')
        response = self.client.get(
            reverse('comments-report', args=(comment.pk,)))
        self.assertEqual(response.status_code, 302)
        [flag] = comment.flags.all()
        self.assertEqual(flag.comment, comment)
        self.assertEqual(flag.user, self.user)
        self.assertTrue('The comment has been reported.'
                        in response.cookies['messages'].value)
