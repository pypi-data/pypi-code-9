from django.core.paginator import Paginator


objects = ['john', 'paul', 'george', 'ringo']
p = Paginator(objects, 2)
page = p.page(2)