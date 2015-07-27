import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.views import login as login_view
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404

from registration.backends.default.views import RegistrationView
from registration import signals

from .forms import *


    
class BaseLoginRegisterView(TemplateView):
    
    template_name = 'account/login_and_register.html'

    def get_context_data(self, **kwargs):
        ctx = super(BaseLoginRegisterView, self).get_context_data(**kwargs)
        ctx['registration_form'] = CreateAccountForm()
        ctx['login_form'] = CustomAuthentication()
        return ctx

    def get(self, request):
        if request.user and request.user.is_authenticated():
            redirect_url = reverse('account_dashboard')            
            return HttpResponseRedirect( redirect_url )

        return super(BaseLoginRegisterView, self).get(request)


class BaseCreateAccount(RegistrationView):
    form_class = CreateAccountForm
    
    next_url = None

    def register(self, request, extra_fields=None, **cleaned_data):
        cleaned_data['username'] = cleaned_data['email']

        self.next_url = cleaned_data['next']

        if not extra_fields:
            extra_fields = {}

        #Add additional fields
        if cleaned_data['first_name']:
            extra_fields['first_name'] = cleaned_data['first_name']
        
        if cleaned_data['last_name']:
            extra_fields['last_name'] = cleaned_data['last_name']
        
        #override simple registration
        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
        self.model.objects.create_user(username, email, password, **extra_fields)
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)

        
        messages.success(request, settings.MESSAGES.get('success_registration',None))
        
        
        return new_user


    def get_success_url(self, request, user):
        if self.next_url:
            return self.next_url
        return reverse('account_dashboard')

    def get(self, request):
        if request.user and request.user.is_authenticated():
            redirect_url = reverse('account_dashboard')            
            return HttpResponseRedirect( redirect_url )

        return super(BaseCreateAccount, self).get(request)


class BaseAccountDashboardView(DetailView):
       
    template_name = "account/dashboard.html"

    def get_object(self):
        return self.request.user

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseAccountDashboardView, self).dispatch(*args, **kwargs)



# ------------------------------------------------------------------------------
# -- Account Management
# ------------------------------------------------------------------------------


class BaseAbstractUserUpdate(UpdateView):
    """
    Abstract User Update
    ====================

    The AbstractUserUpdate view implements common logic needed to automatically
    link a logged in user the record they are updating about themselves. This
    can easily be reused across the account management views.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Decorate dispatch to require user to be logged in."""
        return super(BaseAbstractUserUpdate, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Override Get to user request.user instead of id on query param"""
        self.object = request.user
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        """Override Post to user request.user instead of id on query param"""
        self.object = request.user
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # -- Set Success/Error Messages
        if form.is_valid():
            messages.success(request, settings.MESSAGES.get('success_update_account',None))
            return self.form_valid(form)
        else:
            messages.error(request, settings.MESSAGES.get('input_error',None))
            messages.error(request, str(form.errors))
            return self.form_invalid(form)

    def get_object(self):
        return get_object_or_404(get_user_model(), pk=self.request.user.pk)
            


class BaseAccountUpdate(BaseAbstractUserUpdate):
    """
    Account Update
    ==============

    Update basic account information on the users account.
    """

    
    form_class = AccountUpdateForm
    template_name = 'account/update.html'
    success_url = reverse_lazy('account_update')


        

class BaseAccountUpdateDone(TemplateView):
   
    template_name = "account/update_done.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseAccountUpdateDone, self).dispatch(*args, **kwargs)



class BaseAccountUpdatePassword(BaseAbstractUserUpdate):
    """
    Account Update
    ==============
    """

    
    form_class = PasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('auth_password_change_done')

    def get_form(self, form_class):
        """Pass User to Form"""
        return form_class(self.object, **self.get_form_kwargs())

    def get_form_kwargs(self):
        """Remove Instance"""
        kwargs = super(BaseAccountUpdatePassword, self).get_form_kwargs()
        del kwargs['instance']
        return kwargs




@sensitive_post_parameters()
@csrf_protect
@never_cache
def redirect_login_view(request):
    
    #if user is already logged in, redirect them instead of rendering the login page.
    if request.user and request.user.is_authenticated():
        redirect_url = reverse('account_dashboard')            
        return HttpResponseRedirect( redirect_url )
        
    return login_view(request)



##############################
## ADMIN VIEWS ###############
##############################

class BaseUserDashboardStatsView(ListView):

    # model = User
    template_name = "admin/account/user/dashboard_stats.html"

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(BaseUserDashboardStatsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = self.model._default_manager.all()

        more_link = reverse('admin:account_%s_changelist' % (self.model.__name__.lower()))

        self.registration_list = {
            'title':"Recently Registrations",
            'slug':'recent-registrations',
            'links':queryset.order_by('-date_joined')[:5],
            'more_link_title':"See All Users",
            'more_link':more_link+"?o=-5",
            'display_stat':'date_joined'
        }
        self.login_list = {
            'title':"Recent Logins",
            'slug':'recent-logins',
            'links':queryset.order_by('-last_login')[:5],
            'more_link_title':"See All Users",
            'more_link':more_link+"?o=-6",
            'display_stat':'last_login'
        }
        return [self.registration_list, self.login_list]

