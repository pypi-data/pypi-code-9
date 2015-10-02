import unittest
import payeezy


payeezy.API_KEY = 'y6pWAJNyJyjGv66IsVuWnklkKUPFbb0a'
payeezy.API_SECRET = '86fbae7030253af3cd15faef2a1f4b67353e41fb6799f576b5093ae52901e6f7'
payeezy.TOKEN = 'fdoa-a480ce8951daa73262734cf102641994c1e55e7cdf4c02b6'

tests = [
    ['2499', 'VISA', '4012000033330026', '1218', '123', 'Donald Duck', 'Sale'],
    ['2499', 'VISA', '4005519200000004', '1218', '123', 'Donald Duck', 'Sale']
]

def test_str():
    expected_values = {
        '1': '1',
        '2': '2'
    }
    for method, expected in expected_values.items():
        yield check_str, method, expected

def check_str(method, expected):
    for t in tests:
        assert isinstance(t, str)


def test_data_in_strings(transaction_total, card_type, card_number, card_expiry, card_cvv,
                         cardholder_name, merchant_reference):
    assert isinstance(transaction_total, str)
    assert isinstance(card_type, str)
    assert isinstance(card_number, str)
    assert isinstance(card_expiry, str)
    assert isinstance(card_cvv, str)
    assert isinstance(cardholder_name, str)
    assert isinstance(merchant_reference, str)