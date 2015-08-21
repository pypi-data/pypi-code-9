from django.conf.urls import url

from . import views

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^(?P<question_id>[0-9]+)/$', views.details, name='details'),
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
#     url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
# ]
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name='details'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]