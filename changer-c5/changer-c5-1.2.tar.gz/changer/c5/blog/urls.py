from django.conf.urls import url, patterns

urlpatterns = patterns('changer.c5.blog.views',
    url(r'^(?P<post_id>[0-9]+)/$', 'view_post', name="post-view"),
    url(r'^$', 'list_posts', name="post-lists"),
)
