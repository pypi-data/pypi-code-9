from django.conf import settings
from django.core.cache import cache

from oscar.apps.checkout.views import PaymentDetailsView as BasePaymentDetailsView
from oscar.core.loading import get_model


Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')

MPESA_REFERENCES_CACHE_KEY = 'mpesa_reference_counter'


class MpesaPaymentDetailsView(BasePaymentDetailsView):

    """
    This view has a different chronilogical order for the preview and
    payment_details views.
    """

    template_name = "mpesa/checkout/payment_details.html"

    def get_context_data(self, **kwargs):
        # Get the number the customer should enter as their account number
        ref = self.get_reference_number()
        # Record the reference number used
        self.request.session['mpesa_reference_number'] = ref
        # Construct the template context
        ctx = super(MpesaPaymentDetailsView, self).get_context_data(**kwargs)
        ctx["reference_number"] = ref
        ctx["paybill_number"] = settings.MPESA_PAYBILL_NUMBER
        return ctx

    @staticmethod
    def get_reference_number():
        ref = cache.get(MPESA_REFERENCES_CACHE_KEY)
        if not ref:
            # Get the reference of the last Source
            last_source = Source.objects.only('reference').last()
            if last_source:
                last_ref = last_source.reference
            else:
                # *shrug*
                last_ref = 1005
            ref = int(last_ref) + 1
            cache.set(MPESA_REFERENCES_CACHE_KEY, ref+1)
        else:
            cache.incr(MPESA_REFERENCES_CACHE_KEY)
        return ref

    def post(self, request, *args, **kwargs):
        return self.handle_place_order_submission(request)

    def get_initial_order_status(self, basket):
        return getattr(settings, "OSCAR_INITIAL_ORDER_STATUS", None)

    def handle_payment(self, order_number, order_total, **kwargs):
        # Find the reference number we should expect
        ref = self.request.session['mpesa_reference_number']
        # Find or create the M-Pesa source type
        source_type, _ = SourceType.objects.get_or_create(name='M-Pesa')
        # Associate a new 'M-Pesa' source against this order
        source = Source(source_type=source_type,
                        reference=ref,
                        amount_allocated=order_total.incl_tax,
                        currency="KES")
        self.add_payment_source(source)
