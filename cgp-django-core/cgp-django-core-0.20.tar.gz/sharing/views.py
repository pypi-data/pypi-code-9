import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sites.models import Site
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.views.generic import ListView
from django.views.generic.edit import FormView, FormMixin

from site_admin.dashboard import dashboard_registry, DashboardLoaderModuleRegistry

from monomail.utils import send_monomail

from tracking.models import Event


from .models import *
from .forms import EmailForm, EmailsListField

DEFAULT_DURATION_DAYS = 30

class ShareCounterRedirectView(RedirectView):

    permanent = False
    query_string = True
    
    def get_redirect_url(self, *args, **kwargs):


        full_url = self.request.GET.get('url', None)
        if full_url == None:
            return None

        type = self.request.GET.get('type', None)
        if type == None:
            return None

        title = self.request.GET.get('title', None)
        
        #Retreieve settings
        settings = SocialShareSettings.get_site_settings()
        link_settings = SocialShareLink.objects.get(type=type,parent=settings)

        #Store 
        Event.track( full_url, SHARE_EVENT_CATEOGORY, SHARE_EVENT_ACTION, type)

        #return full_url
        share_url = link_settings._get_share_url(full_url, title)

        return share_url


class EmailFormView(FormView):
    
    form_class = EmailForm
    
    inline_template_name = "sharing/partials/email_form.html"
    inline_template_success_name = "sharing/partials/email_sent_success.html"
    template_name = "sharing/email_form.html"

    def get_form_kwargs(self):
        
        #ADD REFERNCE TO FORM OBJECT
        kwargs = super(EmailFormView, self).get_form_kwargs()

        kwargs['url'] = self.request.GET.get('url', '/')
        kwargs['title'] = self.request.GET.get('title', '')
    
        return kwargs

    def is_inline(self):
        is_inline = 'format' in self.request.REQUEST and self.request.REQUEST['format']=='inline'
        return is_inline


    def get_template_names(self):
        if self.is_inline():
            if self.form_is_valid:
                return [self.inline_template_success_name]
            else:
                return [self.inline_template_name]

        return [self.template_name]

    @property
    def success_url(self):

        redirect_url = self.form.data.get('redirect')
        if redirect_url:
            return redirect_url
        return self.request.META.get('HTTP_REFERER', "/")

    def form_valid(self, form):
        #Store for use in success_url
        self.form = form
        self.form_is_valid = True

      
        ctx_dict = {
            'to_email': form.data.get('to_email'),
            'from_email': form.data.get('from_email'),
            'subject': form.data.get('subject'),
            'message': form.data.get('message'),
            'url': form.data.get('url'),
            'site': Site.objects.get_current()
        }
                

        emails = EmailsListField.SEPARATOR_RE.split(form.data.get('to_email'))
        emails = [email.strip() for email in emails]
        unique_emails = list(set(emails))
        for to_email in unique_emails:
            send_monomail(to_email, settings.SHARING_EMAIL_FORM_TEMPLATE, ctx_dict, settings.SHARING_EMAIL_FORM_CATEGORY)

        #Store 
        Event.track( form.data.get('url'), SHARE_EVENT_CATEOGORY, SHARE_EVENT_ACTION, SocialShareLink.TYPE_EMAIL_FORM)

        if self.is_inline():
            return self.render_to_response(self.get_context_data(form=form))
        else:
            messages.success(self.request, "Thank you for sharing!")
            return super(EmailFormView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.form_is_valid = False
        return super(EmailFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form_is_valid = False
        return super(EmailFormView, self).post(request, *args, **kwargs)

##############################
## ADMIN VIEWS ###############
##############################

def get_latest_shared_paths(queryset, duration_days):
    
    #Get only sharing events:
    queryset.filter(category=SHARE_EVENT_CATEOGORY,action=SHARE_EVENT_ACTION)

    filter_duration = datetime.datetime.now() - datetime.timedelta(days=duration_days)
    queryset = queryset.filter(created__gte=filter_duration)

    path_querset = queryset.values('path').annotate(total=models.Count('path')).order_by('-total')
    
    shared_paths = {
        'title':"Most Shared Paths (Last %s days)"%(duration_days),
        'slug':'most-shared-urls',
        'links':path_querset[:5],
        'more_link_title':"See More",
        'more_link':"%s?%s"%(reverse('dashboard_stats_paths_sharing'), 'days=365'),
        'display_stat':'path',
        'duration_days':duration_days
    }
    return shared_paths

def get_latest_shared_services(queryset, duration_days):
    
    #Get only sharing events:
    queryset.filter(category=SHARE_EVENT_CATEOGORY,action=SHARE_EVENT_ACTION)

    filter_duration = datetime.datetime.now() - datetime.timedelta(days=duration_days)
    queryset = queryset.filter(created__gte=filter_duration)

    service_queryset = queryset.values('label').annotate(total=models.Count('label')).order_by('-total')

    shared_services = {
        'title':"Most Shared Services (Last %s days)"%(duration_days),
        'slug':'most-shared-networks',
        'links':service_queryset[:5],
        'more_link_title':"See More",
        'more_link':"%s?%s"%(reverse('dashboard_stats_services_sharing'), 'days=365'),
        'display_stat':'label',
        'duration_days':duration_days
    }
    return shared_services    

class DashboardStatsView(ListView):

    model = Event
    template_name = "admin/sharing/event/dashboard_stats.html"

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(DashboardStatsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = self.model._default_manager.all()

        #Get only sharing events:
        queryset.filter(category=SHARE_EVENT_CATEOGORY,action=SHARE_EVENT_ACTION)

        duration_days = int(self.request.REQUEST.get('days', DEFAULT_DURATION_DAYS))
        
        self.shared_paths = get_latest_shared_paths(queryset, duration_days)

        self.shared_services = get_latest_shared_services(queryset, duration_days)

        return [self.shared_paths, self.shared_services]


class DashboardMostSharedPathsStatsView(ListView):

    model = Event
    template_name = "admin/sharing/event/dashboard_most_shared_paths_stats.html"

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(DashboardMostSharedPathsStatsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = self.model._default_manager.all()

        #Get only sharing events:
        queryset.filter(category=SHARE_EVENT_CATEOGORY,action=SHARE_EVENT_ACTION)

        self.duration_days = int(self.request.REQUEST.get('days', DEFAULT_DURATION_DAYS))
        
        self.shared_paths = get_latest_shared_paths(queryset, self.duration_days)

        return self.shared_paths['links']


    def get_context_data(self, **kwargs):
        ctx = super(DashboardMostSharedPathsStatsView, self).get_context_data(**kwargs)
        ctx['title'] = self.shared_paths['title']
        ctx['slug'] = self.shared_paths['slug']
        ctx['display_stat'] = self.shared_paths['display_stat']
        ctx['duration_days'] = self.shared_paths['duration_days']
        return ctx


class DashboardMostSharedServicesStatsView(ListView):

    model = Event
    template_name = "admin/sharing/event/dashboard_most_shared_services_stats.html"

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(DashboardMostSharedServicesStatsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = self.model._default_manager.all()

        #Get only sharing events:
        queryset.filter(category=SHARE_EVENT_CATEOGORY,action=SHARE_EVENT_ACTION)

        self.duration_days = int(self.request.REQUEST.get('days', DEFAULT_DURATION_DAYS))
        
        self.shared_services = get_latest_shared_services(queryset, self.duration_days)

        return self.shared_services['links']  

    def get_context_data(self, **kwargs):
        ctx = super(DashboardMostSharedServicesStatsView, self).get_context_data(**kwargs)
        ctx['title'] = self.shared_services['title']
        ctx['slug'] = self.shared_services['slug']
        ctx['display_stat'] = self.shared_services['display_stat']
        ctx['duration_days'] = self.shared_services['duration_days']
        return ctx


dashboard_registry.register(DashboardLoaderModuleRegistry.CATEGORY_COLUMN_THREE, 'Share Stats', 'dashboard_stats_sharing')
