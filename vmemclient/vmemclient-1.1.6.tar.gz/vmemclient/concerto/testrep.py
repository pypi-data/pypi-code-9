#!/usr/bin/env python

import datetime
import pprint
import sys
import time

import vmemclient
from vmemclient.core import error


# Constants
HOST = 'lab-fil3494-mg-a'
SRC_LUN = 'gar-dedup'
DEST_LUN = 'gar-rep'


# Exceptions
class StopTest(Exception):
    pass


# Functions
def create_replication(c):
    oid = c.lun.lun_name_to_object_id(SRC_LUN)
    post_data = {'params': {
        'targetDevice': {
            'dedup': False,
            'thinProvisioning': {'enabled': True},
            'name': 'gar-rep',
            'storagepoolID': 1,
        },
        'policy': {
            'compression': False,
            'microscan': False,
            'encryption': {
                'enabled': False,
            },
        },
        'transferMode': {
            'continuousMode': False,
            'preserveReplicationTimemark': False,
            'useExistingTimemark': False,
        },
        'trigger': {
            'initialTime': '2099-09-09 12:34',
            'interval': '24H',
        },
        'startSync': True,
    }}

    ans = c.basic.post(
        '/logicalresource/replication/{0}'.format(oid),
        post_data,
    )
    return ans

    if not ans['success']:
        raise StopTest(ans['msg'])
    return ans

def update_replication(c):
    oid = c.lun.lun_name_to_object_id(SRC_LUN)
    put_data = {'params': {
        'action': 'update',
        'priority': 500,
        'targetServer': {
            'ipaddress': '10.5.10.67',
            'username': 'root',
            'password': 'ViolinMEM1',
        },
        'transferMode': {
            'continuousMode': False,
            'preserveReplicationTimemark': False,
            'useExistingTimemark': False,
        },
        'trigger': {
            'initialTime': '2099-09-09 12:34',
            'interval': '1H',
            'watermarkRetry': 0,
            'watermarkMB': 0,
        },
        'policy': {
            'compression': False,
            'microscan': False,
            'encryption': {
                'enabled': False,
            },
        },
    }}

    ans = c.basic.put(
        '/logicalresource/replication/{0}'.format(oid),
        put_data,
    )

    if not ans['success']:
        raise StopTest(ans['msg'])
    return ans

def update_replication_minimal(c):
    oid = c.lun.lun_name_to_object_id(SRC_LUN)
    put_data = {'params': {
        'action': 'update',
        'priority': 500,
        'targetServer': {
            'ipaddress': '10.5.10.67',
            'username': 'root',
            'password': 'ViolinMEM1',
        },
    }}

    ans = c.basic.put(
        '/logicalresource/replication/{0}'.format(oid),
        put_data,
    )

    if not ans['success']:
        raise StopTest(ans['msg'])
    return ans

def _replication_action(c, action):
    oid = c.lun.lun_name_to_object_id(SRC_LUN)
    data = {'params': {
        'action': action,
    }}

    ans = c.basic.put(
        '/logicalresource/replication/{0}'.format(oid),
        data,
    )
    return ans

    if not ans['success']:
        raise StopTest(ans['msg'])
    return ans

def sync_replication(c):
    return _replication_action(c, 'sync')

def suspend_replication(c):
    return _replication_action(c, 'suspend')

def resume_replication(c):
    return _replication_action(c, 'resume')

def stop_replication(c):
    return _replication_action(c, 'stop')

def promote_replication(c, force=None):
    oid = c.lun.lun_name_to_object_id(SRC_LUN)
    data = {'params': {
        'action': 'promote',
        'force': bool(force),
    }}

    ans = c.basic.put(
        '/logicalresource/replication/{0}'.format(oid),
        data,
    )
    return ans

    if not ans['success']:
        raise StopTest(ans['msg'])
    return ans

def delete_replication(c, force=None):
    oid = c.lun.lun_name_to_object_id(SRC_LUN)
    data = {
        'force': bool(force),
    }

    ans = c.basic.delete(
        '/logicalresource/replication/{0}'.format(oid),
        data,
    )
    return ans

    if not ans['success']:
        raise StopTest(ans['msg'])
    return ans

def get_last_sync_time(c):
    ans = c.basic.get('/logicalresource/replication/{0}'.format(
        c.lun.lun_name_to_object_id(SRC_LUN)))
    if not ans['success']:
        raise StopTest(ans['msg'])
    ans = ans['data']['replication']['lastSuccessfulSync']
    return ans

def is_replication_running(c):
    return not c.basic.get(
        '/logicalresource/replication/{0}'.format(
            c.lun.lun_name_to_object_id(SRC_LUN),
        ))['data']['replication']['suspended']

def report(msg, refresh=False):
    if refresh:
        sys.stdout.write('\r' + ' '*78 + '\r')
    sys.stdout.write(msg)
    sys.stdout.flush()

def main():
    # Variables

    # Init
    c = vmemclient.open(HOST, 'root', 'ViolinMEM1')
    if c is None:
        print 'No connection object to {0}, quitting'.format(HOST)
        return 1

    # Cleanup (if needed)
    info = c.lun.get_lun_info(SRC_LUN)
    if info['replicationEnabled']:
        print 'Leftover replication detected'
        print 'Last sync time: {0}'.format(get_last_sync_time(c))
        if is_replication_running(c):
            print 'Suspending replication:'
            print suspend_replication(c)
        print 'Deleting replication:'
        print delete_replication(c, True)
    try:
        oid = c.lun.lun_name_to_object_id(DEST_LUN)
    except error.NoMatchingObjectIdError:
        pass
    else:
        print 'Deleting dest lun:'
        print c.lun.delete_lun(force=True, object_id=oid)

    retries = {}
    for x in xrange(50):
        print '\n\nIteration: {0:03}'.format(x)

        report('Creating replication', True)
        while True:
            result = create_replication(c)
            if not result['success']:
                report('.')
                retries.setdefault('create replication', [])
                retries['create replication'].append(
                    (x, result['msg']))
            else:
                break

        sync_time = get_last_sync_time(c)

        report('Suspending replication', True)
        while True:
            result = suspend_replication(c)
            if not result['success']:
                report('.')
                retries.setdefault('suspend replication', [])
                retries['suspend replication'].append(
                    (x, result['msg']))
            else:
                break

        report('Performing replication sync', True)
        while True:
            result = sync_replication(c)
            if not result['success']:
                report('.')
                retries.setdefault('sync replication', [])
                retries['sync replication'].append(
                    (x, result['msg']))
            else:
                break

        report('Waiting for sync', True)
        new_sync_time = sync_time[:]
        while new_sync_time == sync_time:
            report ('.')
            new_sync_time = get_last_sync_time(c)
        retries.setdefault('sync change', [])
        retries['sync change'].append(
            (x, 'From {0} to {1}'.format(sync_time, new_sync_time)))

        report('Promoting replication', True)
        while True:
            result = promote_replication(c)
            if not result['success']:
                report('.')
                retries.setdefault('promote replication', [])
                retries['promote replication'].append(
                    (x, result['msg']))
            else:
                break

        report('Deleting promoted LUN', True)
        while True:
            try:
                c.lun.delete_lun(DEST_LUN, True)
            except error.NoMatchingObjectIdError as e:
                retries.setdefault('delete lun', [])
                retries['delete lun'].append(
                    (x, 'NoMatchingObjectIdError'))
            else:
                break

    c.close()

    print 'Results:'
    pprint.pprint(retries)


if __name__ == '__main__':
    try:
        main()
    except StopTest as e:
        print e
        sys.exit(1)

