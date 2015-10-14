from django.contrib import admin
from django.conf import settings

from changer.c5.blog.models import Post

class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'image']
    list_display = ('pub_date', 'title')

admin.site.register(Post, PostAdmin)
