from django.conf.urls.static import static
from django.conf.urls import patterns, url, include


from .views import *

urlpatterns = patterns('',
    
    url(r'^share-by-email/$', EmailFormView.as_view(), name="share_by_email_view"),

    url(r'^track/shares/$', ShareCounterRedirectView.as_view(), name="share_counter_redirect_view"),
    
    url(r'^admin/dashboard_stats/sharing/events/$', DashboardStatsView.as_view(), name='dashboard_stats_sharing'),
    url(r'^admin/dashboard_stats/sharing/events/paths/$', DashboardMostSharedPathsStatsView.as_view(), name='dashboard_stats_paths_sharing'),
    url(r'^admin/dashboard_stats/sharing/events/services/$', DashboardMostSharedServicesStatsView.as_view(), name='dashboard_stats_services_sharing'),
)
