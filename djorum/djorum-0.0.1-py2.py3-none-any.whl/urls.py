from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(r'^$', views.TopicList.as_view(), name='topics'),
                       url(r'^new_topic/$', views.TopicCreate.as_view(), name='new_topic'),
                       url(r'^(?P<topic_slug>[-\w]+)/$', views.PostList.as_view(), name='topic_posts'),
                       url(r'^(?P<slug>[-\w]+)/edit/$', views.TopicUpdate.as_view(), name='topic_update'),
                       url(r'^(?P<slug>[-\w]+)/delete/$', views.TopicDelete.as_view(), name='topic_delete'),
                       url(r'^(?P<topic_slug>[-\w]+)/new_post/$', views.PostCreate.as_view(), name='new_post'),
                       url(r'^(?P<topic_slug>[-\w]+)/(?P<slug>[-\w]+)/$', views.PostDetail.as_view(), name='post'),
                       url(r'^(?P<topic_slug>[-\w]+)/(?P<slug>[-\w]+)/delete/$', views.PostDelete.as_view(),
                           name='post_delete'),
                       url(r'^(?P<topic_slug>[-\w]+)/(?P<post_slug>[-\w]+)/post/$', views.post_comment,
                           name='post_comment'),
                       url(r'^(?P<topic_slug>[-\w]+)/(?P<post_slug>[-\w]+)/(?P<reply_to_slug>[-\w]+)/reply/$',
                           views.comment_reply,
                           name='comment_reply'),
                       url(r'^(?P<topic_slug>[-\w]+)/(?P<post_slug>[-\w]+)/delete_reply/(?P<reply_id>[-\w]+)/$',
                           views.delete_reply,
                           name='delete_reply')

                       )
