from django.conf import settings
from django.http import HttpResponse
from django.views.generic import CreateView
from django.utils.crypto import constant_time_compare

from .. import models, signals, forms


class IPNReceiverView(CreateView):
    """
    Handler for IPN notification requests.

    This view should always respond with 200, as IPN treats any other status
    as a sign of weakness and repeats the notification.

    IPN sends the notifications as GET requests, but we just treat it as a
    POST request.
    """

    PAYMENT_ACCEPTED_MSG = 'OK|Payment accepted.'
    AUTHENTICATION_FAILURE_MSG = 'FAIL|Paybill authentication failure.'
    MISSING_DATA_ERROR_MSG = "FAIL|The following parameters are missing: %s"
    PAYBILL_ERROR = 'FAIL|Paybill error. Safaricom is experiencing issues.'
    TRANSACTION_ALREADY_EXISTS_MSG = 'FAIL|This notification has already been received'

    model = models.MpesaPayment
    form_class = forms.IPNReceiverForm
    http_method_names = [u'get']

    def authenticate_request(self, request):
        username = request.GET.get("user")
        password = request.GET.get("pass")

        try:
            assert constant_time_compare(username, settings.MPESA_IPN_USER)
            assert constant_time_compare(password, settings.MPESA_IPN_PASS)
        except AssertionError:
            return False

        return True

    def form_invalid(self, form):
        return HttpResponse(self.PAYBILL_ERROR, status=200)

    def form_valid(self, form):
        # Let's save the instance
        self.object = form.save()
        # Notify the processing code
        # TODO Why are we doing this with a signal?
        signals.ipn_received.send(sender=self, mpesa_payment=self.object)
        # Instead of redirect, respond appropriately
        return HttpResponse(self.PAYMENT_ACCEPTED_MSG, status=200)

    def get(self, request, *args, **kwargs):
        if not self.authenticate_request(request):
            return HttpResponse(self.AUTHENTICATION_FAILURE_MSG, status=200)
        # We treat this as a POST request in order to handle the form
        return super(IPNReceiverView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(IPNReceiverView, self).get_form_kwargs()
        # Use GET data instead of POST
        # Convert from immutable QueryDict to dict
        kwargs["data"] = self.request.GET.copy()
        # Copy remaining kwargs to be stored in 'original'
        kwargs["data"]["original"] = kwargs["data"].copy()
        return kwargs
