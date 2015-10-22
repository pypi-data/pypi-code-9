from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from luhublog.models import Author, Entry

from . import app_settings

# class AuthorDetailView(ListView):
# 	model = Author
# 	template_name = "dash/blog/author/author_list.html"

class EntryListView(ListView):
	model = Entry
	context_object_name = "entries"
	template_name = "luhublog/entry_list.html"


class EntryDetailView(DetailView):
	model = Entry
	context_object_name = "entry"
	template_name = "luhublog/entry_detail.html"
