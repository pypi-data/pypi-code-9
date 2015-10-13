# -*- coding: utf-8 -*-
"""some reusable views: inherit from them"""

from django.views.generic.edit import FormView
from decorators import popup_redirect
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied


class PopupRedirectView(FormView):
    """Base class for popup form : redirect if success"""
    template_name = "colorbox/popup_form_base.html"
    form_url = ""
    title = ""
    form_class = None
    success_url = ""
    staff_only = False
    
    def get_context_data(self, **kwargs):
        """update template context"""
        context = super(PopupRedirectView, self).get_context_data(**kwargs)
        context['form_url'] = self.get_form_url()
        context['title'] = self.get_title()
        return context

    def get_form_url(self):
        """get url for submitting the form"""
        return self.form_url
    
    def get_title(self):
        """get title"""
        return self.title
    
    @method_decorator(popup_redirect)
    def dispatch(self, *args, **kwargs):
        """Manage permissions and use decorator for redirection"""
        if self.staff_only:
            if not self.request.user.is_staff:
                raise PermissionDenied
        return super(PopupRedirectView, self).dispatch(*args, **kwargs)


class AdminPopupRedirectView(PopupRedirectView):
    """Popup for admin"""
    staff_only = True
    
    #@method_decorator(popup_redirect)
    def dispatch(self, *args, **kwargs):
        """check permission and don't redirect"""
        if self.staff_only:
            if not self.request.user.is_staff:
                raise PermissionDenied()
        return super(AdminPopupRedirectView, self).dispatch(*args, **kwargs)