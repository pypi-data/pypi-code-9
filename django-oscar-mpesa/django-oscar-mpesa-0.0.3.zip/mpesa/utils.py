import datetime
import decimal
import random
import string

from django.conf import settings


TRANSACTION_DATE_FORMAT = "%d/%m/%y"
TRANSACTION_TIME_FORMAT = "%I:%M %p"


def generate_phonenumber():
    return "254770%0.6d" % random.randint(0, 999999)


def generate_mpesa_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def generate_text(**kwargs):
    return ("{mpesa_code} Confirmed. on {mpesa_trx_date} at "
                "{mpesa_trx_time} Ksh{mpesa_amt} received from "
                "{mpesa_sender} {mpesa_msisdn}. Account Number {mpesa_acc} "
                "New Utility balance is Ksh{balance}"
    ).format(
        balance=str(decimal.Decimal(kwargs['mpesa_amt']) * 15),
        **kwargs
    )


def create_ipn_data(data={}):
    now = datetime.datetime.now()
    # Set initial values
    msg = {
        "id": random.randint(0, 8**8),
        "orig": "MPESA",
        'routemethod_id': '2',
        'routemethod_name': 'HTTP',
        "dest": generate_phonenumber(),
        "tstamp": str(now),
        "mpesa_code": generate_mpesa_code(),
        "mpesa_msisdn": generate_phonenumber(),
        "mpesa_sender": "JOHN SMITH",
        "mpesa_amt": "10.0",
        "mpesa_acc": "1337",
        "customer_id": 2040,
        "business_number": settings.MPESA_PAYBILL_NUMBER,
        "mpesa_trx_date": now.date().strftime(TRANSACTION_DATE_FORMAT),
        "mpesa_trx_time": now.time().strftime(TRANSACTION_TIME_FORMAT),
        "user": settings.MPESA_IPN_USER,
        "pass": settings.MPESA_IPN_PASS
    }
    # Override with provided dict
    msg.update(data)
    # Add text property
    msg['text'] = generate_text(**msg)
    return msg
