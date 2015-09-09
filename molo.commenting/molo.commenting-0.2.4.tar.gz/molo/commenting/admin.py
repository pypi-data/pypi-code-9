from django.contrib import admin

from molo.commenting.models import MoloComment
from django_comments.models import CommentFlag


admin.site.register(MoloComment)
admin.site.register(CommentFlag)
