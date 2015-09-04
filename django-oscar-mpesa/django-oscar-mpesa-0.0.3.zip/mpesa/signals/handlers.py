from django.db import transaction
from django.dispatch import receiver

from oscar.apps.checkout.signals import post_checkout
from oscar.core.loading import get_model

from . import ipn_received, unknown_payment_received
from .. import processing
from ..models import MpesaPayment


Source = get_model("payment", "Source")


@receiver(post_checkout)
@transaction.atomic()
def process_created_order(sender, order, **kwargs):
    """
    This receives the signal sent out after an order has been created
    successfully. We iterate over outstanding transactions check if any
    payments for that order have been made.

    A `payment_accepted` signal is sent for each payment successfully matched
    to an order. The signal handler should associate each payment with the
    order and determine the correct status.
    """
    # Check whether the user selected M-Pesa
    source = order.sources.filter(source_type__name="M-Pesa").first()
    if source:
        # Look for any existing payments that match the reference
        mpesa_payments = MpesaPayment.objects.filter(mpesa_acc=source.reference)
        # Associate those payments with this source
        for payment in mpesa_payments:
            processing.allocate_payment_to_source(payment, source)


@receiver(ipn_received)
@transaction.atomic()
def process_payment_notification(sender, **kwargs):
    payment = kwargs['mpesa_payment']
    # Get the source associated with the MPesa account number
    source = Source.objects.filter(reference=payment.mpesa_acc).first()
    if source:
        processing.allocate_payment_to_source(payment, source)
    else:
        # MPesa account number does not match any order
        unknown_payment_received.send(sender="payment_processor",
                                      payment=payment)
