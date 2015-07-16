from lisa_api.api.tts import base
import subprocess
import tempfile
from lisa_api.lisa.logger import logger


class Pico(base.TTSBase):
    """Use picotts
    """

    def convert(self, message, lang="en"):
        """Convert the text to sound and return this sound.

        :param message: A string containing the message
        :type message: str
        :param lang: The lang to use
        :type lang: str
        :returns: Audio data.
        """
        combined_sound = []

        tempwav = tempfile.NamedTemporaryFile(suffix=".wav")
        tempmp3 = tempfile.NamedTemporaryFile(suffix=".mp3")

        if 'en' in lang:
            language = 'en-US'
        else:
            language = '-'.join([str(lang), str(lang).upper()])
        try:
            commandwav = ['pico2wave', '-w', tempwav.name, '-l', language, '--', message]
            logger.debug("Command used to generate the wav sound : %s in the file %s" % (commandwav, tempwav.name))
            logger.debug(subprocess.check_output(commandwav, stderr=subprocess.STDOUT))
            commandmp3 = ['avconv', '-y', '-f', 'wav', '-i', tempwav.name, '-b:a', '256k', '-f', 'mp3', tempmp3.name]
            logger.debug("Command used to generate the mp3 sound : %s in the file %s" % (commandmp3, tempmp3.name))
            logger.debug(subprocess.check_output(commandmp3, stderr=subprocess.STDOUT))
        except subprocess.CalledProcessError as error:
            logger.error('Problem generating sound')
            logger.debug('Output : %s' % str(error.output))
            return False
        combined_sound.append(tempmp3.read())
        tempwav.close()
        tempmp3.close()
        return b"".join(combined_sound)
