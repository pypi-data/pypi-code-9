from functools import partial
import json
import logging
from ambisafe.containers import Container

logger = logging.getLogger('ambisafe')


class Transaction(object):
    def __init__(self, hex, fee, sighashes, operator_signatures=None, user_signatures=None):
        self.hex = hex
        self.fee = fee
        self.sighashes = sighashes
        self.operator_signatures = operator_signatures or []
        self.user_signatures = user_signatures or []

    def to_dict(self):
        return {
            'hex': self.hex,
            'fee': self.fee,
            'sighashes': self.sighashes,
            'operator_signatures': self.operator_signatures,
            'user_signatures': self.user_signatures,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class RecoveryTransaction(Transaction):
    def __init__(self, operator, recovery_transaction, account_id):
        self.account_id = account_id

        self.operator_container = Container.from_server_response(operator['publicKey'], operator['data'],
                                                                 operator['iv'], operator['salt'])
        super(RecoveryTransaction, self).__init__(**recovery_transaction)

    def to_json(self):
        return json.dumps(super(RecoveryTransaction, self).to_dict())

    def sign(self, secret):
        sign_func = partial(self.operator_container.sign, private_key=self.operator_container.get_private_key(secret))
        self.operator_signatures = map(sign_func, self.sighashes)
