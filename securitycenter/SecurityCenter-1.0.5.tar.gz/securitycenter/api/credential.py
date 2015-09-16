from six import iteritems
from ._base import Module, extract_value
from ..exc import ValidationError


class Credential(Module):
    _name = 'credential'

    @extract_value('credentials')
    def init(self):
        return self._request('init')

    def _add(self, type, name, description, tag, **kwargs):
        kwargs.update({'type': type, 'name': name, 'description': description, 'tags': tag})
        return self._request('add', kwargs)

    def add_windows(self, name, username, password, domain=None, description=None, tag=None):
        return self._add(
            'windows', name=name, description=description, tag=tag,
            username=username, password=password, domain=domain
        )

    def add_ssh(self, name, username, password=None, public_key=None, private_key=None, passphrase=None, escalation='none', escalation_username=None, escalation_password=None, description=None, tag=None):
        if public_key is not None:
            public_key = self._sc.file.name_or_upload(public_key)

        if private_key is not None:
            private_key = self._sc.file.name_or_upload(private_key)

        return self._add(
            'ssh', name=name, description=description, tag=tag,
            username=username, password=password,
            publicKey=public_key, privateKey=private_key, passphrase=passphrase,
            privilegeEscalation=escalation, escalationUsername=escalation_username, escalationPassword=escalation_password
        )

    def add_snmp(self, name, community, description=None, tag=None):
        return self._add(
            'snmp', name=name, description=description, tag=tag,
            communityString=community
        )

    def add_kerberos(self, name, ip, port, protocol, realm, description=None, tag=None):
        return self._add(
            'kerberos', name=name, description=description, tag=tag,
            ip=ip, port=port, protocol=protocol, realm=realm
        )

    def add_database(self, name, login, password, db_type, sid=None, port=None, oracle_auth_type=None, sql_server_auth_type=None, description=None, tag=None):
        return self._add(
            'database', name=name, description=description, tag=tag,
            login=login, password=password, dbType=db_type, sid=sid, port=port,
            OracleAuthType=oracle_auth_type, SQLServerAuthType=sql_server_auth_type
        )

    def _edit(self, type, id, prefill=True, simulate=True, name=None, description=None, tag=None, **kwargs):
        if prefill == True:
            try:
                input = next(c for c in self.init() if int(c['id'] == id))
            except StopIteration:
                raise ValidationError('unable to find existing credential {}'.format(id))
        elif prefill:
            input = dict(prefill)
        else:
            input = {'id': id}

        kwargs.update({'type': type, 'name': name, 'description': description, 'tag': tag})
        input.update((k, v) for k, v in iteritems(kwargs) if v is not None)
        action = 'editSimulate' if simulate else 'edit'
        return self._request(action, input)

    def edit_windows(self, id, prefill=True, simulate=True, name=None, description=None, tag=None, username=None, password=None, domain=None):
        return self._edit(
            'windows', id, prefill=prefill, simulate=simulate,
            name=name, description=description, tag=tag,
            username=username, password=password, domain=domain
        )

    def edit_ssh(self, id, prefill=True, simulate=True, name=None, description=None, tag=None, username=None, password=None, public_key=None, private_key=None, passphrase=None, escalation=None, escalation_username=None, escalation_password=None):
        if public_key is not None:
            public_key = self._sc.file.name_or_upload(public_key)

        if private_key is not None:
            private_key = self._sc.file.name_or_upload(private_key)

        return self._edit(
            'ssh', id, prefill=prefill, simulate=simulate,
            name=name, description=description, tag=tag,
            username=username, password=password,
            publicKey=public_key, privateKey=private_key, passphrase=passphrase,
            privilegeEscalation=escalation, escalationUsername=escalation_username, escalationPassword=escalation_password
        )

    def edit_snmp(self, id, prefill=True, simulate=True, name=None, description=None, tag=None, community=None):
        return self._edit(
            'snmp', id, prefill=prefill, simulate=simulate,
            name=name, description=description, tag=tag,
            communityString=community
        )

    def edit_kerberos(self, id, prefill=True, simulate=True, name=None, description=None, tag=None, ip=None, port=None, protocol=None, realm=None):
        return self._edit(
            'kerberos', id, prefill=prefill, simulate=simulate,
            name=name, description=description, tag=tag,
            ip=ip, port=port, protocol=protocol, realm=realm
        )

    def edit_database(self, id, prefill=True, simulate=True, name=None, description=None, tag=None, login=None, password=None, db_type=None, sid=None, port=None, oracle_auth_type=None, sql_server_auth_type=None):
        return self._edit(
            'database', id, prefill=prefill, simulate=simulate,
            name=name, description=description, tag=tag,
            login=login, password=password, dbType=db_type, sid=sid, port=port,
            OracleAuthType=oracle_auth_type, SQLServerAuthType=sql_server_auth_type
        )

    @extract_value()
    def share(self, id, group_ids, simulate=True):
        r = self._request('shareSimulate' if simulate else 'share', {
            'id': id,
            'groups': [{'id': gid} for gid in group_ids]
        })
        r['_key'] = 'effects' if simulate else None
        return r

    @extract_value()
    def delete(self, ids, simulate=True):
        r = self._request('deleteSimulate' if simulate else 'delete', {
            'credentials': [{'id': id} for id in ids]
        })
        r['_key'] = 'effects' if simulate else 'credentials'
        return r
