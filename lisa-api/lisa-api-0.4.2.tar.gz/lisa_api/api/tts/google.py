from lisa_api.api.tts import base
import re
import requests
from lisa_api.lisa.logger import logger


class Google(base.TTSBase):
    """Use googletts
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

        try:
            # process text into chunks
            text = message.replace('\n', '')
            text_list = re.split('(\.)', text)
            combined_text = []
            for idx, val in enumerate(text_list):
                if idx % 2 == 0:
                    combined_text.append(val)
                else:
                    joined_text = ''.join((combined_text.pop(), val))
                    if len(joined_text) < 100:
                        combined_text.append(joined_text)
                    else:
                        subparts = re.split('( )', joined_text)
                        temp_string = ""
                        temp_array = []
                        for part in subparts:
                            temp_string += part
                            if len(temp_string) > 80:
                                temp_array.append(temp_string)
                                temp_string = ""
                            # append final part
                        temp_array.append(temp_string)
                        combined_text.extend(temp_array)
                # download chunks and write them to the output file
            for idx, val in enumerate(combined_text):
                headers = {"Host": "translate.google.com",
                           "Referer": "https://translate.google.com/",
                           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36"}
                r = requests.get("https://translate.google.com/translate_tts?ie=UTF-8&tl=%s&q=%s&total=%s&idx=%s&client=t&prev=input" % (
                    lang, val, len(combined_text), idx), headers=headers)
                if r.status_code is not requests.codes.ok:
                    logger.error('There was an error with google TTS')
                    return False
                else:
                    combined_sound.append(r.content)
        except:
            logger.error('There was an error with google TTS')
            return False

        return b"".join(combined_sound)
