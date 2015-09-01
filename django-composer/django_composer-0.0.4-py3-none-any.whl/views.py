"""
views.py
"""
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.conf import settings
from django.core.exceptions import PermissionDenied

from .models import Element


def default_can_compose_permission(view, request, template_name):
    """
    Default global permission check.
    """
    return request.user and request.user.is_authenticated and (
        request.user.is_staff or request.user.is_superuser)


class ComposerPermissionMixin:
    def can_compose_permission(self, request, template_name):
        """
        Can be overridden at the view level to provide view specific permission
        checks. Otherwise, the global permission check is permformed.
        """
        perm = getattr(settings, 'COMPOSER_CAN_COMPOSE_PERMISSION', default_can_compose_permission)
        return perm(self, request, template_name)


class ComposerViewMixin(ComposerPermissionMixin):
    """
    View mixin for any Django CBV that uses `django.views.generic.base.ContextMixin`
    and `django.views.views.generic.TemplateResponseMixin`.
    """

    def get_context_data(self, **context):
        """
        Get the available compose elements for this view if allowed.
        """
        context = super().get_context_data(**context)

        template = self.get_template_names()[0]

        context['can_compose_permission'] = self.can_compose_permission(self.request, template)
        context['template_name'] = template
        context['composer_elements'] = {e.name: e
                                        for e in Element.objects.filter(template_name=template)}

        return context


class EditComposerElementView(ComposerPermissionMixin, SingleObjectMixin, TemplateView):
    """
    Ajax friendly view for editing a composer element.
    """
    model = Element
    template_name = 'composer/edit.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Only allow users with permission.
        """
        self.object = self.get_object()
        if not self.can_compose_permission(request, self.object.template_name):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **context):
        """
        Add the composer element.
        """
        context['element'] = self.object

        if self.object.is_dynamic and self.object.context_example is not None:
            context['context_example'] = '<br>'.join(self.object.context_example.split('\n'))

        if 'content' not in context:
            context['content'] = self.object.content

        return context

    def post(self, request, *args, **kwargs):
        """
        Update the contents if they render correctly.
        """
        ctx = {}
        status = 200
        content = request.POST.get('content', '')
        
        try:
            self.object.attempt_update(content, request.user)
        except self.model.TemplateError as e:
            ctx = {'error': str(e), 'content': content}
            status = 400

        return self.render_to_response(self.get_context_data(**ctx), status=status)


class ExampleView(ComposerViewMixin, TemplateView):
    """
    Shows an example of different usages of composer elements on a static page.
    """
    template_name = 'composer/example.html'
