#!/usr/bin/env python
# coding=utf-8

from pykafka import KafkaClient

from .exceptions import SubmanException


class SubmanProducer(object):
    def __init__(self, kafka_hosts):
        self.client = KafkaClient(hosts=kafka_hosts)
        if not self.client:
            raise SubmanException("connect kafka server{}".format(kafka_hosts))

    def send(self, topic_name, messages):
        if topic_name not in self.client.topics:
            raise SubmanException("kafka topic({}) not exist".format(topic_name))

        kafka_topic = self.client.topics[topic_name]
        producer = kafka_topic.get_producer()
        producer.produce(messages)
