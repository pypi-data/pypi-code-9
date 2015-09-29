from sqlalchemy import types
from moneyed import Money as MoneyBehaviour


class Money(types.TypeDecorator):
    impl = types.Float

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.FLOAT)

    def process_bind_param(self, value, dialect):
        return float(value)

    def process_result_value(self, value, dialect):
        return Decimal(value)
