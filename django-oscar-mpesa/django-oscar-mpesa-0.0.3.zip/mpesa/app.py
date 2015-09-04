from django.conf import settings
from django.conf.urls import url, include

from oscar.core.application import Application

from . import views
from .dashboard.app import application as mpesa_dashboard_app

class MpesaApp(Application):

    name = "mpesa"

    def get_urls(self):
        urls = [
            url(r'^checkout/mpesa/', views.MpesaPaymentDetailsView.as_view(),
                name="payment-details"),
            url(r'^mpesa/ipn/$', views.IPNReceiverView.as_view(),
                name="ipn-receiver"),
            url(r'^dashboard/mpesa/', include(mpesa_dashboard_app.urls)),
        ]
        return self.post_process_urls(urls)

application = MpesaApp()
