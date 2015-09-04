from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import get_model

from .. import utils


MpesaPayment = get_model("mpesa", "MpesaPayment")


class PaymentsListView(ListView):
    model = MpesaPayment
    template_name = "mpesa/dashboard/payments-list.html"
    context_object_name = "payments"


class PaymentDetailView(DetailView):

    model = MpesaPayment
    template_name = "mpesa/dashboard/payment-detail.html"
    context_object_name = "payment"


class IPNGeneratorView(TemplateView):

    template_name = "mpesa/dashboard/generator.html"

    def get_context_data(self, **kwargs):
        ctx = super(IPNGeneratorView, self).get_context_data(**kwargs)
        ctx['ipn'] = utils.create_ipn_data()
        return ctx
