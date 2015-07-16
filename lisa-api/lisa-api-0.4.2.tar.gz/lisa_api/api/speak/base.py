import abc
import six


@six.add_metaclass(abc.ABCMeta)
class SpeakBase(object):
    """Base class for Speak
    """

    @abc.abstractmethod
    def send_message(self, message, zone='all', source='api'):
        """Send a text message.

        :param message: A string containing the message
        :type message: str
        :param zone: The zone where the message will be sent
        :type lang: str
        :param source: The zone where the message came from
        :type lang: str
        :returns: True or False.
        :rtype: Boolean
        """
