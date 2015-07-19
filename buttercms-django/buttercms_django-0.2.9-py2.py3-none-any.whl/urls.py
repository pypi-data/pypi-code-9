from django.conf.urls import patterns, url

from .feeds import LatestPostFeed, AtomBlogPostFeed
from .views import BlogHome, BlogPost, AuthorPage, CategoryPage

urlpatterns = [
    url(r'^$', BlogHome.as_view(), name='blog'),

    # Feeds
    url(r'^rss/$', LatestPostFeed(), name='blog_rss'),
    url(r'^atom/$', AtomBlogPostFeed(), name='blog_atom'),
    
    url(r'^page/(?P<page>\d+)$', BlogHome.as_view(), name='archive'),
    url(r'^author/(?P<author_slug>.*)$', AuthorPage.as_view(), name='blog_author'),
    url(r'^category/(?P<category_slug>.*)$', CategoryPage.as_view(), name='blog_category'),
    # This must appear last since it's a catch all
    url(r'^(?P<slug>.*)$', BlogPost.as_view(), name='blog_post'),
]