from oscar.core.loading import get_model, get_class

PaymentEventType = get_model("order", "PaymentEventType")


def fulfil_order(sender, **kwargs):
    transaction = kwargs.get("transaction")

    order = transaction.source.order

    event_type, _ = PaymentEventType.objects.get_or_create(name="PAID")

    EventHandler = get_class("order.processing", "EventHandler")
    event_handler = EventHandler()
    event_handler.handle_payment_event(order, event_type, transaction.amount,
                                       lines=[], line_quantities=[])
