import json
import time

import kafka

import logging

logging.basicConfig()

kafka_url = "192.168.10.4:9092"

client = kafka.client.KafkaClient(kafka_url)
producer = kafka.producer.KeyedProducer(
    client,
    async=False,
    req_acks=kafka.producer.KeyedProducer.ACK_AFTER_LOCAL_WRITE,
    ack_timeout=2000)

consumer = kafka.consumer.SimpleConsumer(
    client,
    str(time.time()),
    "transformed-events",
    auto_commit=True,
    max_buffer_size=None)

consumer.seek(0, 2)
consumer.provide_partition_info()
consumer.fetch_last_known_offsets()

event = [
    {
        u'_context_request_id': u'req-5f6ec633-d3e4-4aec-b952-5a2feeaa21ae',
        u'_context_quota_class': None,
        u'event_type': u'compute.instance.update',
        u'_context_auth_token': u'6e2a9a607eb04643aded6a9970f8ce6c',
        u'_context_user_id': u'542562',
        u'payload': {
            u'state_description': u'unrescuing',
            u'availability_zone': None,
            u'terminated_at': u'',
            u'ephemeral_gb': 0,
            u'instance_type_id': 2,
            u'bandwidth': {

            },
            u'deleted_at': u'',
            u'reservation_id': u'res-239577',
            u'memory_mb': 512,
            u'display_name': u'Instance_216142',
            u'hostname': u'server-500432',
            u'state': u'rescued',
            u'old_state': u'rescued',
            u'launched_at': u'2015-07-21 15:43:35.709431',
            u'metadata': {

            },
            u'node': u'node-436156',
            u'ramdisk_id': u'',
            u'access_ip_v6': u'3018: 1377: 96f4: 0e6f: 12ee: a011: 245f: ce77',
            u'disk_gb': 20,
            u'access_ip_v4': u'143.179.252.190',
            u'kernel_id': u'',
            u'host': u'host-340688',
            u'user_id': u'542562',
            u'image_ref_url': u'http: //171.161.171.145: 9292/images/ece696b6-0b5f-490c-afc8-0a1cf2f687a0',
            u'audit_period_beginning': u'2015-07-21 01:41:54.709431',
            u'root_gb': 20,
            u'tenant_id': u'transform_func_test',
            u'created_at': u'2014-12-23 11:48:59.709431',
            u'old_task_state': None,
            u'instance_id': u'62c46649-a07d-4705-845b-a271fe0ce2c4',
            u'instance_type': u'512MBStandardInstance',
            u'vcpus': 1,
            u'image_meta': {
                u'os_distro': u'centos',
                u'org.openstack__1__os_distro': u'org.centos',
                u'image_type': u'base',
                u'container_format': u'ovf',
                u'min_ram': u'512',
                u'cache_in_nova': u'True',
                u'min_disk': u'20',
                u'disk_format': u'vhd',
                u'auto_disk_config': u'True',
                u'os_type': u'linux',
                u'org.openstack__1__os_version': u'6.4',
                u'org.openstack__1__architecture': u'x64'
            },
            u'architecture': u'x64',
            u'new_task_state': u'unrescuing',
            u'audit_period_ending': u'2015-07-21 15:47:36.709431',
            u'os_type': u'linux',
            u'instance_flavor_id': u'2'
        },
        u'priority': u'INFO',
        u'_context_is_admin': False,
        u'_context_user': u'542562',
        u'publisher_id': u'publisher-701331',
        u'message_id': u'3ccf82a3-9639-4047-a109-9e9d0f6d04e9',
        u'_context_remote_address': u'150.155.252.251',
        u'_context_roles': [
            u'checkmate',
            u'object-store: default',
            u'compute: default',
            u'identity: user-admin'
        ],
        u'timestamp': u'2015-07-21 15:33:03.069431',
        u'_context_timestamp': u'2015-07-21 15:47:04.193431',
        u'_unique_id': u'3410ada0f1814f258fef9bd1a6d2533e',
        u'_context_glance_api_servers': None,
        u'_context_project_name': u'916988',
        u'_context_read_deleted': u'no',
        u'_context_tenant': u'916988',
        u'_context_instance_lock_checked': False,
        u'_context_project_id': u'916988',
        u'_context_user_name': u'542562'
    }
]

monasca_event = {}
monasca_event['event'] = event

conf = [{'event_type': 'compute.instance.*',
         'traits': {'tenant_id': {'fields': 'payload.tenant_id'},
                    'service': {'fields': 'publisher_id',
                                'plugin': 'split'}}}]


def send(topic, msg):
    key = "ABCD"
    producer.send(topic, key, json.dumps(msg))


def add(_id):
    print("Add transform definition {}".format(_id))
    msg = {}
    msg['transform_id'] = _id
    msg['transform_definition'] = conf
    print msg
    send("transform-definitions", msg)


def delete(_id):
    print("Delete transform definition {}".format(_id))
    msg = {}
    msg['transform_id'] = _id
    msg['transform_definition'] = []
    send("transform-definitions", msg)


def wait_for_events(num):
    rx_events = 0
    expected_key_set = [u'event_type', u'service', u'tenant_id', u'when', u'request_id', u'message_id']
    data = consumer.get_messages(count=1000, timeout=5)
    for e in data:
        partition = e[0]
        consumer.commit([partition])
        event_payload = json.loads(e[1].message.value)
        print ""
        print event_payload
        print ""
        if event_payload['tenant_id'] == "transform_func_test":
            if len(event_payload.keys()) == 6:
                rx_events += 1
            else:
                print("Event has invalid key set")
                print("Expected: {}".format(expected_key_set))
                print("Recieved: {}".format(event_payload.keys()))

    return rx_events


def test_transform():
    expected_events = 3

    add('A')
    add('B')

    time.sleep(2)
    send("raw-events", monasca_event)

    rx_events = 0
    rx_events += wait_for_events(2)

    delete('A')
    time.sleep(2)
    send("raw-events", monasca_event)

    rx_events += wait_for_events(1)

    delete('B')

    if rx_events == expected_events:
        print("Transform success.  Expected {} found {}".
              format(expected_events, rx_events))
    else:
        print("Transform failure.  Expected {} found {}".
              format(expected_events, rx_events))

test_transform()
