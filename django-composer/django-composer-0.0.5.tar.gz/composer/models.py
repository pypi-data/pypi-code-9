"""
models.py
"""
import datetime

from django.db import models
from django.conf import settings
from django.template import Template, Context, TemplateSyntaxError


class Element(models.Model):
    """
    Contains text/template to be injected into pages.
    """
    template_name = models.CharField(max_length=200)
    name = models.CharField(max_length=100)

    is_dynamic = models.BooleanField(default=False)
    last_changed = models.DateTimeField(auto_now=True)
    has_changed = models.BooleanField(default=False)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    context_example = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'composer'
        index_together = ('name', 'template_name')
        unique_together = ('name', 'template_name')

    class TemplateError(Exception):
        pass

    def save(self, *args, **kwargs):
        """
        Update timestamp automatically.
        """
        self.last_changed = datetime.datetime.now()
        return super().save(*args, **kwargs)

    def render(self, default_content, context=None):
        """
        Dynamic templates are actually rendered using the Django template
        engine, while static templates are just returned as-is.

        The default_content will be displayed as-is if this element hasn't been
        changed before.
        """
        if not self.has_changed:
            return str(default_content)
        
        if not self.is_dynamic:
            return self.content

        tpl = Template(self.content)
        return tpl.render(Context(context or {}))

    def attempt_update(self, new_content, changed_by):
        """
        Attempt to update this element with new content.
        """
        self.has_changed = True

        if self.is_dynamic:
            try:
                Template(new_content).render(Context({}))
            except TemplateSyntaxError as e:
                raise self.TemplateError(str(e))

        self.content = new_content
        self.changed_by = changed_by
        self.has_changed = True
        self.save()
