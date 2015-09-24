#!/usr/bin/env python
# coding=utf-8

from pykafka import KafkaClient
from .exceptions import SubmanException

__all__ = ["SubmanConsumer"]


class SubmanConsumer(object):
    def __init__(self, kafka_hosts, zookeeper_hosts=None):
        self.kafka_hosts = kafka_hosts
        self.zookeeper_hosts = zookeeper_hosts
        self.kafka_client = KafkaClient(hosts=self.kafka_hosts)

    def C(self, topic_name, group_id,
          auto_commit_enable=True,
          zookeeper_connect=None, **kafka_kwargs):

        if not zookeeper_connect:
            zookeeper_connect = self.zookeeper_hosts

        if not zookeeper_connect:
            raise SubmanException("please set zookeeper_connect")

        def _consumer(func):
            if topic_name not in self.kafka_client.topics:
                raise SubmanException(
                    """
                        please create topic !
                        ./bin/kafka-topics.sh --create
                            --topic {topic_name}
                            --partitions {partitions}
                            --replication-factor {replication_factor}
                            --zookeeper {zookeeper_client}
                    """)

            kafka_kwargs["auto_commit_enable"] = auto_commit_enable
            kafka_kwargs["zookeeper_connect"] = zookeeper_connect

            self.topic = self.kafka_client.topics[topic_name]
            self.group_id = group_id
            self.consumer_func = func
            self.kafka_kwargs = kafka_kwargs
        return _consumer

    def run(self):
        if not self.topic:
            raise SubmanException("please using @C(topic_name, group_id)")

        balanced_consumer = self.topic.get_balanced_consumer(
            self.group_id, **self.kafka_kwargs)

        while True:
            message = balanced_consumer.consume()
            self.consumer_func(
                message.value,
                topic=self.topic,
                group_id=self.group_id,
                message_partition=message.partition,
                message_partition_id=message.partition_id,
                message_offset=message.offset)
