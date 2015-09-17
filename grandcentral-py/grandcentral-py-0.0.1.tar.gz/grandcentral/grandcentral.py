from collections import defaultdict
import json


class GrandCentral(object):
    """
    An extremely basic publisher subscriber event library. It provides only
    two methods
    a)publish - it publishes an event on provided channel with a payload
    b) subscribe: it registers channel/event pair with a consumer that is to be called
    when that particular event is published on the channel.
    """

    def __init__(self):
        self.task_methods = defaultdict(defaultdict)

    def subscribe(self, channel, event, consumer):
        """
        Registers a grandcentralconsumer. A consumer

        :param module:
        :return:
        """

        if event not in self.task_methods[channel]:
            self.task_methods[channel][event] = []

        self.task_methods[channel][event].append(consumer)

    def publish(self, channel, event, data):
        """
        This emits an even to a 'channel' for an 'event' with some serializable
        'data'.

        :param channel: Channel name. str type.
        :param event: Event name. str type.
        :param data: A simple object which should be serializable.
        :return:
        """
        if not channel in self.task_methods or \
                not event in self.task_methods[channel]:
            return

        data['event_name'] = event;

        for consumer in self.task_methods[channel][event]:
            consumer.consume(channel, event, data)


class DjangoGrandCentral(GrandCentral):
    def register_django_signal(self, channel, event_name, django_signal,
                               sender=None):

        def receiver_func(sender, **kwargs):
            payload = kwargs
            payload['sender'] = sender.__name__
            if 'instance' in kwargs:
                payload['instance'] = payload['instance'].pk

            if 'signal' in kwargs:
                del payload['signal']

            self.publish(channel, event_name, payload)

        django_signal.connect(receiver_func, sender=sender, weak=False)


class GrandCentralConsumer(object):
    """
    Base class for any consumer that wants to consume Grand Central events.

    """
    def __init__(self, task):
        self.task = task

    def consume(self, payload):
        """
        This is the method called to consume data from an event in a channel.

        :param payload: The data dict that came from the event. Also contains the
        name of the event.

        :return: Nothing
        """
        raise NotImplementedError()


class SyncConsumer(GrandCentralConsumer):
    """
    A simple synchronous consumer that calls the receiver immidiately
    """

    def consume(self, payload):
        self.task(payload)


class CeleryConsumer(GrandCentralConsumer):
    """
    A simple consumer that executes the task asynchronously using celery
    """

    def consume(self, payload):
        self.task.delay(payload)
