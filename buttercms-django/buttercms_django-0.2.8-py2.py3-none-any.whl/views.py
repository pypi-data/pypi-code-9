from django.conf import settings
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView

from api import ButterCms


class BlogHome(TemplateView):

    default_template_name = "buttercms_blog.html"

    def get_template_names(self):
        try:
            # Check for an overridden template.
            return [settings.BLOG_BASE]
        except AttributeError:
            # Use default if BLOG_BASE is not defined.
            return [self.default_template_name]

    def get_context_data(self, **kwargs):
        context = super(BlogHome, self).get_context_data(**kwargs)

        # Check if page was passed via url match.
        try:
            page = kwargs['page']
        except:
            page = None

        butter = ButterCms()
        response = butter.get_posts(page)
        context['next_page'] = response['next_page']
        context['previous_page'] = response['previous_page']
        context['recent_posts'] = response['results']
        return context


class BlogPost(TemplateView):

    default_template_name = "buttercms_blog_post.html"

    def get_template_names(self):
        """ Check if there's a custom blog post template. """
        try:
            # Check for an overridden template.
            return [settings.BLOG_POST]
        except AttributeError:
            # Use default if BLOG_POST is not defined.
            return [self.default_template_name]

    def get_context_data(self, **kwargs):
        context = super(BlogPost, self).get_context_data(**kwargs)

        try:
            # Check for an overridden blog template.
            context['base_template'] =  settings.BLOG_BASE
        except AttributeError:
            context['base_template'] =  'buttercms_blog.html'

        butter = ButterCms()
        context['post'] = butter.get_post(kwargs['slug'])
        context['post']['body'] = mark_safe(context['post']['body'])
        return context


class AuthorPage(TemplateView):

    default_template_name = "buttercms_blog_author.html"

    def get_template_names(self):
        """ Check if there's a custom blog post template. """
        try:
            # Check for an overridden template.
            return [settings.BLOG_AUTHOR]
        except AttributeError:
            # Use default if BLOG_AUTHOR is not defined.
            return [self.default_template_name]

    def get_context_data(self, **kwargs):
        context = super(AuthorPage, self).get_context_data(**kwargs)

        try:
            # Check for an overridden blog template.
            context['base_template'] =  settings.BLOG_BASE
        except AttributeError:
            context['base_template'] =  'buttercms_blog.html'


        butter = ButterCms()
        response = butter.get_author(kwargs['author_slug'])
        context['first_name'] = response['first_name']
        context['last_name'] = response['last_name']
        context['recent_posts'] = response['recent_posts']
        return context


class CategoryPage(TemplateView):

    default_template_name = "buttercms_blog_category.html"

    def get_template_names(self):
        """ Check if there's a custom blog post template. """
        try:
            # Check for an overridden template.
            return [settings.BLOG_CATEGORY]
        except AttributeError:
            # Use default if BLOG_CATEGORY is not defined.
            return [self.default_template_name]

    def get_context_data(self, **kwargs):
        context = super(CategoryPage, self).get_context_data(**kwargs)

        try:
            # Check for an overridden blog template.
            context['base_template'] =  settings.BLOG_BASE
        except AttributeError:
            context['base_template'] =  'buttercms_blog.html'


        butter = ButterCms()
        response = butter.get_category(kwargs['category_slug'])
        context['category_name'] = response['name']
        context['recent_posts'] = response['recent_posts']
        return context