from six import iteritems
from ._base import Module, extract_value
from securitycenter.exc import ValidationError


class Scan(Module):
    _name = 'scan'

    @extract_value('scans')
    def init(self):
        return self._request('init')

    @extract_value('scan')
    def add(self, name, description=None, policy=None, plugin=None, assets=None, ips=None, credentials=None, repository=None, zone=None, reports=None, mitigated_age=0, dhcp=False, virtual=False, schedule=None, frequency='now', timeout='import', rollover='template', mail_launch=False, mail_finish=False):
        if plugin is not None:
            type = 'plugin'
            policy_id = None
        else:
            type='policy'
            policy_id = policy
            policy = None

        return self._request('add', {
            'name': name,
            'description': description,
            'type': type,
            'policy': policy,
            'policyID': policy_id,
            'pluginID': plugin,
            'assets': [{'id': a_id} for a_id in assets] if assets else None,
            'ipList': ','.join(ips) if ips else None,
            'credentials': [{'id': c_id} for c_id in credentials] if reports else None,
            'repositoryID': repository,
            'zoneID': zone,
            'reports': [{'id': r_id} for r_id in reports] if reports else None,
            'classifyMitigatedAge': mitigated_age,
            'dhcpTracking': dhcp,
            'scanningVirtualHosts': virtual,
            'scheduleDefinition': schedule,
            'scheduleFrequency': frequency,
            'timeoutAction': timeout,
            'rolloverType': rollover,
            'emailOnLaunch': mail_launch,
            'emailOnFinish': mail_finish
        })

    @extract_value('scan')
    def edit(self, id, name=None, description=None, policy=None, plugin=None, assets=None, ips=None, credentials=None, repository=None, zone=None, reports=None, mitigated_age=None, dhcp=None, virtual=None, schedule=None, frequency=None, timeout=None, rollover=None, mail_launch=None, mail_finish=None):
        try:
            input = next(c for c in self.init() if int(c['id'] == id))
        except StopIteration:
            raise ValidationError('unable to find existing scan {}'.format(id))

        if plugin is not None:
            type = 'plugin'
            policy_id = None
        else:
            type='policy'
            policy_id = policy
            policy = None

        input.update((k, v) for k, v in iteritems({
            'name': name,
            'description': description,
            'type': type,
            'policy': policy,
            'policyID': policy_id,
            'pluginID': plugin,
            'assets': [{'id': a_id} for a_id in assets] if assets else None,
            'ipList': ','.join(ips) if ips else None,
            'credentials': [{'id': c_id} for c_id in credentials] if reports else None,
            'repositoryID': repository,
            'zoneID': zone,
            'reports': [{'id': r_id} for r_id in reports] if reports else None,
            'classifyMitigatedAge': mitigated_age,
            'dhcpTracking': dhcp,
            'scanningVirtualHosts': virtual,
            'scheduleDefinition': schedule,
            'scheduleFrequency': frequency,
            'timeoutAction': timeout,
            'rolloverType': rollover,
            'emailOnLaunch': mail_launch,
            'emailOnFinish': mail_finish
        }) if v is not None)

        return self._request('edit', input)

    @extract_value('scan')
    def copy(self, id, name, user=None):
        return self._request('copy', {
            'id': id,
            'name': name,
            'targetUserID': user
        })

    @extract_value()
    def delete(self, ids, simulate=True):
        r = self._request('deleteSimulate' if simulate else 'delete', {
            'scans': [{'id': s_id} for s_id in ids]
        })
        r['_key'] = 'effects' if simulate else 'scans'
        return r

    @extract_value('scanResult')
    def launch(self, id):
        return self._request('launch', {
            'scanID': id
        })


class ScanResult(Module):
    _name = 'scanResult'

    @extract_value('scanResults')
    def init(self, group_id=None, start=None, end=None):
        return self._request('init', {
            'groupID': group_id,
            'startTime': start,
            'endTime': end
        })

    @extract_value('scanResults')
    def get_range(self, start, end, group=None):
        return self._request('getRange', {
            'startTime': start,
            'endTime': end,
            'groupID': group
        })

    def copy(self, ids, users=None, emails=None):
        return self._request('copy', {
            'resultID': ids,
            'userID': users,
            'email': ','.join(emails) if emails else None
        })

    @extract_value()
    def delete(self, ids, simulate=True):
        r = self._request('deleteSimulate' if simulate else 'delete', {
            'scanResults': [{'id': r_id} for r_id in ids]
        })
        r['_key'] = 'effects' if simulate else 'scanResults'
        return r

    def download(self, id, type='v2'):
        return self._request('download', {
            'scanResultID': id,
            'downloadType': type
        }, parse=False).content

    def import_result(self, id, mitigated_age=0, dhcp=False, virtual=False):
        return self._request('import', {
            'scanResultID': id,
            'classifyMitigatedAge': mitigated_age,
            'dhcpTracking': dhcp,
            'scanningVirtualHosts': virtual
        })

    @extract_value('scanResults')
    def pause(self, id):
        return self._request('pause', {
            'scanResultID': id
        })

    @extract_value('scanResults')
    def resume(self, id):
        return self._request('resume', {
            'scanResultID': id
        })

    def stop(self, id, type='discard'):
        return self._request('stop', {
            'scanResultID': id,
            'type': type
        })

    @extract_value('purgeCount')
    def purge(self, older_than='now', simulate=True):
        return self._request('purgeSimulate' if simulate else 'purge', {
            'olderThan': older_than
        })

    def get_progress(self, id, completed=False):
        return self._request('getProgress', {
            'scanResultID': id,
            'includeCompleted': completed
        })


class NessusResult(Module):
    _name = 'nessusResults'

    def upload(self, file, repo_id, mitigate_age=0, dhcp=False, virtual=False):
        return self._request('upload', {
            'filename': self._sc.file.name_or_upload(file),
            'repID': repo_id,
            'classifyMitigatedAge': mitigate_age,
            'dhcpTracking': dhcp,
            'scanningVirtualHosts': virtual
        })
