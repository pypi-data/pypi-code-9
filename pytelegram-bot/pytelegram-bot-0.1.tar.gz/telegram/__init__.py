import requests
import io


class TelegramException(Exception):
    pass


class Telegram(object):
    def __init__(self, api_key):
        self._url = "https://api.pytelegram-bot.org/bot" + api_key

    def _get(self, method):
        response = requests.get(self._url + method)
        result = response.json()
        if not result['ok']:
            raise TelegramException(result['description'])
        return result['result']

    def _post(self, method, data, files=None):
        response = requests.post(self._url + method, data=data, files=files)
        result = response.json()
        if not result['ok']:
            raise TelegramException(result['description'])
        return result['result']

    def test(self):
        """
        A simple method for testing your bot's auth token. Requires no parameters.
        Returns basic information about the bot in form of a User object.

        Returns:

            If works properly, returns the following dictionary.

                {'id': int, 'username': str, 'first_name': str}

            If not, raises an exception

        Raises:
            TelegramException: if an error was detected.

        """
        return self._get('/getMe')

    def get_updates(self):
        """
        Use this method to receive incoming updates using long polling. An Array of Update objects is returned.

        Returns:
            An array containing last 24 hours updates. For example:
            [{'message': {'message_id': int, 'date': int,
                          'chat': {'last_name': str, 'id': int, 'first_name': str},
                          'from': {'last_name': str, 'id': int, 'first_name': str},
                          'text': str},
              'update_id': int}]

        Raises:
            TelegramException: if an error was detected.
         """

        return self._get('/getUpdates')

    def send_message(self, chat_id, text, disable_web_page_preview=False, reply_to_message_id=None):
        """

        Sends a message

        Args:
            chat_id (int): Chat identification number where to send the message. Note that the bot cannot initialize a
                chat or group.
            text (str): The message itself.
            disable_web_page_preview (Optional[bool]): if the text message contains a link, do not previsualice it.
            reply_to_message_id (Optional[int]): Message identification to which we are answering.

        Returns:
            If everything goes ok. The message itself:
            {'message_id': int, 'date': int, 'text': str,
             'chat': {'last_name': str, 'id': int, 'first_name': str},
             'from': {'id': int, 'username': str, 'first_name': str}}

        Raises:
            TelegramException: if an error was detected.

        """

        data = {'chat_id': chat_id, 'text': text, 'disable_weg_page_preview': disable_web_page_preview,
                'reply_to_message_id': reply_to_message_id}
        return self._post('/sendMessage', data)

    def forward_message(self, chat_id, from_chat_id, message_id):
        """

        Use this method to forward messages of any kind. On success, the sent Message is returned.

        Args:
            chat_id (int): Chat ID where to send the message
            from_chat_id (int): User or GroupChat ID where the message was seen for first time.
            message_id (int): Unique message identifier

        Returns:
            If everything goes ok. The message itself:
            {'message_id': int, 'date': int, 'text': str,
             'chat': {'last_name': str, 'id': int, 'first_name': str},
             'from': {'id': int, 'username': str, 'first_name': str}}

        Raises:
            TelegramException: if an error was detected.

        """
        data = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
        return self._post('/forwardMessage', data)

    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send photos. On success, the sent Message is returned.

        Args:
            chat_id (int): Unique identifier for the message recipient — User or GroupChat id
            photo (str): Photo to send. You can either pass a file_id as str to resend a photo that is already on the
                Telegram servers, or upload a new photo using multipart/form-data.
            caption (Optional[str]): Photo caption (may also be used when resending photos by file_id).
            reply_to_message_id (Optional[int]): If the message is a reply, ID of the original message
            reply_markup (Optional[str]): Additional interface options. A JSON-serialized object for a custom reply
                keyboard, instructions to hide keyboard or to force a reply from the user.

        Returns:
            If everything goes ok. The message itself:
            {'from': {'username': str, 'first_name': str, 'id': int},
             'caption': str,
             'chat': {'last_name': str, 'first_name': str, 'id': int},
             'photo': [{'file_id': str, 'file_size': int, 'height': int, 'width': int}],
             'message_id': int, 'date': int}

        Raises:
            TelegramException: if an error was detected.
        """
        files = None
        data = {'chat_id': chat_id, 'caption': caption, 'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup}
        if isinstance(photo, io.BufferedIOBase):
            files = {'photo': photo}
        elif isinstance(photo, str):
            data['photo'] = photo
        else:
            raise TelegramException('Photo should be either a string or a binary object')
        return self._post('/sendPhoto', data, files)

    def send_audio(self, chat_id, audio, duration=None, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice
        message. For this to work, your audio must be in an .ogg file encoded with OPUS (other formats may be sent as
        Document). On success, the sent Message is returned.
        Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.

        Args:
            chat_id (int): Unique identifier for the message recipient — User or GroupChat id
            audio (str): Audio file to send. You can either pass a file_id as String to resend an audio that is already
                on the Telegram servers, or upload a new audio file using multipart/form-data.
            duration (Optional[int]): Duration of sent audio in seconds
            reply_to_message_id (Optional[int]): If the message is a reply, ID of the original message
            reply_markup (Optional[str]): Additional interface options. A JSON-serialized object for a custom reply
                keyboard, instructions to hide keyboard or to force a reply from the user.

        Returns:
            If everything goes ok. The message itself:
            {'message_id': int,
             'from': {'username': str, 'first_name': str, 'id': int},
             'date': int,
             'chat': {'first_name': str, 'id': int, 'last_name': str},
             'audio': {'duration': int, 'mime_type': str, 'file_id': str, 'file_size': int}}

        Raises:
            TelegramException: if an error was detected.
        """
        files = None
        data = {'chat_id': chat_id, 'duration': duration, 'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup}
        if isinstance(audio, io.BufferedIOBase):
            files = {'audio': audio}
        elif isinstance(audio, str):
            data['audio'] = audio
        else:
            raise TelegramException('Audio should be either a string or a binary object')
        return self._post('/sendAudio', data, files)

    def send_document(self, chat_id, document, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send general files. On success, the sent Message is returned.
        Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.

        Args:
            chat_id (int): Unique identifier for the message recipient — User or GroupChat id
            document (str): File to send. You can either pass a file_id as String to resend a
                file that is already on the Telegram servers, or upload a new file using multipart/form-data.
            reply_to_message_id (Optional[int]): If the message is a reply, ID of the original message
            reply_markup (Optional[str]): Additional interface options. A JSON-serialized object for a custom reply
                keyboard, instructions to hide keyboard or to force a reply from the user.

        Returns:
            If everything goes ok. The message itself:
            {'message_id': int,
             'chat': {'id': int, 'first_name': str, 'last_name': str},
             'document': {'file_size': int, 'file_id': str, 'file_name': str},
             'from': {'id': int, 'first_name': str, 'username': str},
             'date': int}

        Raises:
            TelegramException: if an error was detected.
        """
        files = None
        data = {'chat_id': chat_id, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}
        if isinstance(document, io.BufferedIOBase):
            files = {'document': document}
        elif isinstance(document, str):
            data['document'] = document
        else:
            raise TelegramException('Document should be either a string or a binary object')
        return self._post('/sendDocument', data, files)

    def send_sticker(self, chat_id, sticker, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send .webp stickers. On success, the sent Message is returned.

        Args:
            chat_id (int): Unique identifier for the message recipient — User or GroupChat id
            sticker (str): Sticker to send. You can either pass a file_id as String to resend a sticker that is
                already on the Telegram servers, or upload a new sticker using multipart/form-data.
            reply_to_message_id (Optional[int]): If the message is a reply, ID of the original message
            reply_markup (Optional[str]): Additional interface options. A JSON-serialized object for a custom reply
                keyboard, instructions to hide keyboard or to force a reply from the user.

        Returns:
            If everything goes ok. The message itself:
            {'date': int,
             'from': {'first_name': str, 'id': int, 'username': str},
             'chat': {'first_name': str, 'id': int, 'last_name': str},
             'sticker': {'file_id': str, 'height': int,
                         'thumb': {'width': int, 'file_id': str, 'file_size': int, 'height': int},
                         'width': int, 'file_size': int},
             'message_id': int}

        Raises:
            TelegramException: if an error was detected.
        """
        files = None
        data = {'chat_id': chat_id, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}
        if isinstance(sticker, io.BufferedIOBase):
            files = {'sticker': sticker}
        elif isinstance(sticker, str):
            data['sticker'] = sticker
        else:
            raise TelegramException('Sticker should be either a string or a binary object')
        return self._post('/sendSticker', data, files)

    def send_video(self, chat_id, video, duration=None, caption=None, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send video files, Telegram clients support mp4 videos (other formats may be sent as
        Document). On success, the sent Message is returned.
        Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.

        Args:
            chat_id (int): Unique identifier for the message recipient — User or GroupChat id
            video (str): Video to send. You can either pass a file_id as String to resend a video
                that is already on the Telegram servers, or upload a new video file using multipart/form-data.
            duration (Optional[int]): Duration of sent video in seconds
            caption (Optional[str]): Video caption (may also be used when resending videos by file_id).
            reply_to_message_id (Optional[int]): If the message is a reply, ID of the original message
            reply_markup (Optional[str]): Additional interface options. A JSON-serialized object for a custom reply
                keyboard, instructions to hide keyboard or to force a reply from the user.

        Returns:
            If everything goes ok. The message itself:
            {'video': {'file_id': str, 'height': int, 'width': int, 'duration': int, 'file_size': int},
             'date': int,
             'from': {'id': int, 'first_name': str, 'username': str},
             'message_id': int,
             'chat': {'id': int, 'first_name': str, 'last_name': str}}

        Raises:
            TelegramException: if an error was detected.
        """
        files = None
        data = {'chat_id': chat_id, 'duration': duration, 'caption': caption,
                'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}
        if isinstance(video, io.BufferedIOBase):
            files = {'video': video}
        elif isinstance(video, str):
            data['video'] = video
        else:
            raise TelegramException('Video should be either a string or a binary object')
        return self._post('/sendVideo', data, files)

    def send_location(self, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send point on the map. On success, the sent Message is returned.

        Args:
            chat_id (int): Unique identifier for the message recipient — User or GroupChat id
            latitude (float): Latitude of location
            longitude (float): Longitude of location
            reply_to_message_id (Optional[int]): If the message is a reply, ID of the original message
            reply_markup (Optional[str]): Additional interface options. A JSON-serialized object for a custom reply
                keyboard, instructions to hide keyboard or to force a reply from the user.

        Returns:
            If everything goes ok. The message itself:
            {'message_id': int,
             'date': int,
             'from': {'id': int, 'first_name': str, 'username': str},
             'chat': {'id': int, 'first_name': str, 'last_name': str},
             'location': {'longitude': float, 'latitude': float}}


        Raises:
            TelegramException: if an error was detected.
        """
        data = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude,
                'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}
        return self._post('/sendLocation', data)

        # sendChatAction
        # getUserProfilePhotos
        # setWebhook

    def send_chataction(self, chat_id, action):
        """
        Use this method when you need to tell the user that something is happening on the bot's side.
        The status is set for 5 seconds or less (when a message arrives from your bot,
        Telegram clients clear its typing status).

        Args:
            chat_id (int): Unique identifier for the message recipient — User or GroupChat id
            action (str): Type of action to broadcast. Choose one, depending on what the user
                is about to receive: typing for text messages, upload_photo for photos, record_video or
                upload_video for videos, record_audio or upload_audio for audio files,
                upload_document for general files, find_location for location data.

        Returns:
            'bool': success or failure

        Raises:
            TelegramException: if an error was detected.
        """
        data = {'chat_id': chat_id, 'action': action}
        return self._post('/sendChatAction', data)

    def get_userprofilephotos(self, user_id, offset=None, limit=None):
        """
        Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos object.

        Args:
            user_id (int): Unique identifier of the target user
            offset (Optional[int]): Sequential number of the first photo to be returned. By default,
                all photos are returned.
            limit (Optional[int]): Limits the number of photos to be retrieved. Values between 1—100 are accepted.
                Defaults to 100.

        Returns:
            {'total_count': int,
             'photos': [[{'file_size': int, 'height': int, 'file_id': str, 'width': int}]]}

        Raises:
            TelegramException: if an error was detected.
        """
        data = {'user_id': user_id, 'offset': offset, 'limit': limit}
        return self._post('/getUserProfilePhotos', data)

    def set_webhook(self, url=None):
        """
        Use this method to specify a url and receive incoming updates via an outgoing webhook.
        Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url,
        containing a JSON-serialized Update. In case of an unsuccessful request, we will give up after a reasonable
        amount of attempts.

        If you'd like to make sure that the Webhook request comes from Telegram, we recommend using a secret path in
        the URL, e.g. www.example.com/<token>. Since nobody else knows your bot‘s token, you can be pretty sure it’s us.

        Args:
            url (Optional[str]): HTTPS url to send updates to. Use an empty string to remove webhook integration

        Returns:
            'bool': success or failure

        Raises:
            TelegramException: if an error was detected.
        """

        data = {'url': url}
        return self._post('/setWebhook', data)
