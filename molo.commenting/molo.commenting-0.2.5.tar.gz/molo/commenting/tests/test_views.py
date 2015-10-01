from datetime import datetime

from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase, Client, override_settings

from molo.commenting.models import MoloComment
from molo.commenting.forms import MoloCommentForm
from molo.core.models import ArticlePage


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

    def test_reporting_without_removal(self):
        comment = self.mk_comment('the comment')
        response = self.client.get(
            reverse('molo-comments-report', args=(comment.pk,)))
        self.assertEqual(response.status_code, 302)
        [flag] = comment.flags.all()
        self.assertEqual(flag.comment, comment)
        self.assertEqual(flag.user, self.user)
        self.assertFalse(MoloComment.objects.get(pk=comment.pk).is_removed)
        self.assertTrue('The comment has been reported.'
                        in response.cookies['messages'].value)

    def test_reporting_with_removal(self):
        comment = self.mk_comment('the comment')
        with self.settings(COMMENTS_FLAG_THRESHHOLD=1):
            response = self.client.get(
                reverse('molo-comments-report', args=(comment.pk,)))
        self.assertEqual(response.status_code, 302)
        [flag] = comment.flags.all()
        self.assertEqual(flag.comment, comment)
        self.assertEqual(flag.user, self.user)
        self.assertTrue(MoloComment.objects.get(pk=comment.pk).is_removed)
        self.assertTrue('The comment has been reported.'
                        in response.cookies['messages'].value)

    def test_molo_post_comment(self):
        data = MoloCommentForm(self.user, {}).generate_security_data()
        data.update({
            'name': 'the supplied name',
            'comment': 'Foo',
        })
        self.client.post(
            reverse('molo-comments-post'), data)
        [comment] = MoloComment.objects.filter(user=self.user)
        self.assertEqual(comment.comment, 'Foo')
        self.assertEqual(comment.user_name, 'the supplied name')

    def test_molo_post_comment_anonymous(self):
        data = MoloCommentForm(self.user, {}).generate_security_data()
        data.update({
            'name': 'the supplied name',
            'comment': 'Foo',
            'submit_anonymously': '1',
        })
        self.client.post(
            reverse('molo-comments-post'), data)
        [comment] = MoloComment.objects.filter(user=self.user)
        self.assertEqual(comment.comment, 'Foo')
        self.assertEqual(comment.user_name, 'Anonymous')
        self.assertEqual(comment.user_email, self.user.email)

    def test_molo_post_comment_without_email_address(self):
        self.user.email = ''
        self.user.save()

        data = MoloCommentForm(self.user, {}).generate_security_data()
        data.update({
            'name': 'the supplied name',
            'comment': 'Foo',
        })
        self.client.post(
            reverse('molo-comments-post'), data)
        [comment] = MoloComment.objects.filter(user=self.user)
        self.assertEqual(comment.comment, 'Foo')
        self.assertEqual(comment.user_name, 'the supplied name')
        self.assertEqual(comment.user_email, 'blank@email.com')


@override_settings(ROOT_URLCONF='molo.commenting.tests.test_views')
class ViewMoreArticleCommentsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'test', 'test@example.org', 'test')
        self.article = ArticlePage.objects.create(
            title='article 1', depth=1,
            subtitle='article 1 subtitle',
            slug='article-1', path=[1])

        for i in range(50):
            MoloComment.objects.create(
                content_type=ContentType.objects.get_for_model(self.article),
                object_pk=self.article.pk,
                content_object=self.article,
                site=Site.objects.get_current(),
                user=self.user,
                comment='comment %s' % (i,),
                submit_date=datetime.now())

    def test(self):
        client = Client()
        response = client.get(
            reverse('more-comments', args=[self.article.pk, ],))
        self.assertContains(response, 'Page 1 of 3')
        self.assertContains(response, '&rarr;')
        self.assertNotContains(response, '&larr;')

        response = client.get(
            '%s?p=2' % (reverse('more-comments', args=[self.article.pk, ],),))
        self.assertContains(response, 'Page 2 of 3')
        self.assertContains(response, '&rarr;')
        self.assertContains(response, '&larr;')

        response = client.get(
            '%s?p=3' % (reverse('more-comments', args=[self.article.pk, ],),))
        self.assertContains(response, 'Page 3 of 3')
        self.assertNotContains(response, '&rarr;')
        self.assertContains(response, '&larr;')
