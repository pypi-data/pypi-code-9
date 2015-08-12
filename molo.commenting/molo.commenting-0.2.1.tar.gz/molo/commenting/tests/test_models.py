from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase

from molo.commenting.models import MoloComment


class MoloCommentTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'test', 'test@example.org', 'test')
        self.content_type = ContentType.objects.get_for_model(self.user)

    def mk_comment(self, comment):
        return MoloComment.objects.create(
            content_type=self.content_type,
            object_pk=self.user.pk,
            content_object=self.user,
            site=Site.objects.get_current(),
            user=self.user,
            comment=comment,
            submit_date=datetime.now())

    def test_parent(self):
        first_comment = self.mk_comment('first comment')
        second_comment = self.mk_comment('second comment')
        second_comment.parent = first_comment
        second_comment.save()
        [child] = first_comment.children.all()
        self.assertEqual(child, second_comment)
