from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from oscar.core.application import Application

from . import views


class MpesaDashboardApplication(Application):
    name = 'dashboard'

    default_permissions = ['is_staff', ]

    def get_urls(self):
        urls = [
            url(r"^payments/$", views.PaymentsListView.as_view(),
                name="payments-list"),
            url(r"^payment/(?P<pk>\d+)/$", views.PaymentDetailView.as_view(),
                name="payment-detail"),
            url(r"^generator/$", views.IPNGeneratorView.as_view(),
                name="generator"),
        ]
        return self.post_process_urls(urls)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = MpesaDashboardApplication()
