from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from slugify import slugify

from .models import Category, Product, ProductBase

class DocumentationList(ListView):
    model = Product
    template_name = 'simplesjop/documentation-list.html'

    def get_queryset(self):
        return self.model.objects.all()


class CategoriesListView(ListView):
    model = Category
    template_name = 'simplesjop/category-list.html'

    def get_queryset(self):
        return self.model.objects.all()


class ProductsListView(DetailView):
    model = Category
    template_name = 'simplesjop/product-list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['products'] = self.object.products.all()
        return context


class ProductDetailView(DetailView):
    model = ProductBase
    template_name = 'simplesjop/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['versions'] = self.object.versions.all()
        return context


def checkout(request):
    """
    Redirect after checkout lands here, do anything if needed
    """
    return HttpResponseRedirect('/')