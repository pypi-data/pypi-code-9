# -*- coding: utf-8 -*-
"""
    field.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
import copy
import os

from trytond.model.fields import Function, Field
from trytond.config import config
from trytond.transaction import Transaction
from cryptography.fernet import Fernet


class EncryptedField(Function):
    """Encrypted field uses a symmetric encryption
    technique to store data. Secret key is stored in tryton configuration
    file as below::

        [encrypted_field]
        secret_key = thisisverysecretkey

    """
    supported_types = ('char', 'text', 'selection')

    def __init__(self, field):
        '''
        :param field: The field of the function.
        '''
        if field._type not in self.supported_types:
            raise NotImplementedError(
                'EncryptedField does not support %s type fields' % field._type
            )
        if hasattr(field, 'translate') and field.translate:
            raise RuntimeError('Encrypted field cannot be translated')

        super(EncryptedField, self).__init__(field, self.get, True, True)

    __init__.__doc__ += Field.__init__.__doc__

    def __copy__(self):
        return EncryptedField(copy.copy(self._field))

    def __deepcopy__(self, memo):
        return EncryptedField(copy.deepcopy(self._field))

    def sql_type(self):
        return self._field.sql_type()

    @classmethod
    def _encrypt(cls, raw):
        """
        Return encrypted raw_text
        """
        if raw is None:
            return None

        key = os.environ.get('TRYTOND_ENCRYPTED_FIELD__SECRET_KEY') or \
            config.get('encrypted_field', 'secret_key')
        return Fernet(key).encrypt(raw.encode('utf-8'))

    @classmethod
    def _decrypt(cls, encrypted):
        """
        Return decrypted encrypted_text
        """
        if encrypted is None:
            return None

        key = os.environ.get('TRYTOND_ENCRYPTED_FIELD__SECRET_KEY') or \
            config.get('encrypted_field', 'secret_key')
        return Fernet(key).decrypt(encrypted.encode('utf-8'))

    def set(self, model, name, ids, value, *args):
        assert args == (), "Not implemented yet"

        cursor = Transaction().cursor
        sql_table = model.__table__()
        column = getattr(sql_table, self.name)

        args = iter((ids, value) + args)
        for ids, value in zip(args, args):
            cursor.execute(*sql_table.update(
                columns=[column],
                values=[self._encrypt(value)],
                where=sql_table.id.in_(ids))
            )

    def get(self, ids, Model, name, values=None):
        cursor = Transaction().cursor
        sql_table = Model.__table__()

        cursor.execute(
            *sql_table.select(
                sql_table.id,
                getattr(sql_table, self.name),
                where=sql_table.id.in_(ids)
            )
        )

        return {
            self.name: dict(
                (r[0], self._decrypt(r[1])) for r in cursor.fetchall()
            )
        }

    def convert_domain(self, domain, tables, Model):
        """
        Return a SQL expression for the domain using tables

        The only valid value to search for is None. This helps to determine if
        a value was set or not.

        Because Fernet encryption is not deterministic (the same source
        text encrypted using the same key will result in a different
        encrypted token each time). So searching is not possible for
        encrypted data in any way.
        """
        name, operator, value = domain
        assert value is None, \
            'Encrypted fields can only be searched for existence of data only'

        return self._field.convert_domain(domain, tables, Model)
