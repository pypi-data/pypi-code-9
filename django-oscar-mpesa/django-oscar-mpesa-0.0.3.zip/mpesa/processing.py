from oscar.core.loading import get_model

from . import models, signals


Transaction = get_model("payment", "Transaction")


def allocate_payment_to_source(payment, source):
    # Update the source total
    source.amount_debited += payment.mpesa_amt
    source.save()
    # Create a transaction for this payment
    transaction = source.transactions.create(txn_type=Transaction.DEBIT,
                                             amount=payment.mpesa_amt,
                                             reference=payment.mpesa_acc,
                                             status=models.PAYMENT_RECEIVED)
    # Broadcast the wonderful news
    signals.payment_accepted.send(sender="payment_processor",
                                  transaction=transaction)
