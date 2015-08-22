# coding: utf-8

from collections import defaultdict


class EventsDispatcher(object):
    """
    Event dispatcher.
    """

    def __init__(self):
        self.handlers = defaultdict(list)

    def send(self, event):
        """
        :param event: Event object.
        :type event: Event

        :return: Handlers responses.
        :rtype: list
        """
        return [
            handler(sender=event.sender, *event.args, **event.kwargs)
            for sender, handler in self.handlers[event.__class__]
            if sender is None or sender is event.sender]

    def connect(self, handler, clazz, sender=None):
        """
        Connects handler by event class or event name.

        :param handler: Event handler.
        :type handler: callable
        :param clazz: Event class.
        :type clazz: type[Event]
        :param sender: Event sender or None.
        :type sender: object|None
        """
        self.handlers[clazz].append((sender, handler))

    def disconnect(self, handler, clazz, sender=None):
        """
        Disconnects handler by event class or event name.

        :param handler: Event handler.
        :type handler: callable
        :param clazz: Event class.
        :type clazz: type[Event]
        :param sender: Event sender or None.
        :type sender: object|None
        """
        try:
            while True:
                self.handlers[clazz].remove((sender, handler))
        except ValueError:
            pass


class Event(object):
    """
    Event class, sent by EventDispatcher.
    """
    def __init__(self, *args, **kwargs):
        """
        :param sender: Event sender or None.
        :type sender: object|None
        :param args: List args.
        :type args: list
        :param kwargs: Keyword args.
        :type kwargs: dict
        """
        self.sender = kwargs.pop('sender', None)
        self.args = args
        self.kwargs = kwargs
