# stevedore/example/base.py
import abc

import six


@six.add_metaclass(abc.ABCMeta)
class TTSBase(object):
    """Base class for TTS plugin
    """

    @abc.abstractmethod
    def convert(self, message, lang="en_US"):
        """Convert the text to sound and return this sound.

        :param message: A string containing the message
        :type message: str
        :param lang: The lang to use
        :type lang: str
        :returns: Audio data.
        """
