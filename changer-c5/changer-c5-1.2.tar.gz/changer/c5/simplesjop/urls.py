from django.conf.urls import patterns, url

from .views import  DocumentationList, CategoriesListView, ProductsListView, ProductDetailView


urlpatterns = patterns('',
                       url(r'^$',
                           CategoriesListView.as_view(), name='list-categories'),

                       url(r'^(?P<slug>.+)/$',
                           ProductsListView.as_view(), name="list-products"),

                       url(r'^(?P<category_path>.*)(?P<pk>\d+)/(?P<product_slug>.+)$',
                           ProductDetailView.as_view(), name="product"),

                       url(r'^documentation/?$',
                          DocumentationList.as_view(), name="list-documentation"),
                       
                       url(r'^checkout/?$',
                           'changer.c5.simplesjop.views.checkout',
                           name="sjop-checkout"),
                       )