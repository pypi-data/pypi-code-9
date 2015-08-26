#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Mikhail Baranov'

import json
import hashlib

import requests

API_ENDPOINT = 'https://api.ringcloud.ru'
TIMEOUT = 60


class RingCloudError(RuntimeError):
    pass


class RingCloud(object):
    def __init__(self, api_key, password):
        self.api_endpoint = API_ENDPOINT
        self.api_key = str(api_key)
        self.password = str(password)
        self.hash = hashlib.md5(self.api_key.encode('utf-8') + self.password.encode('utf-8')).hexdigest()
        self.auth = '?api_key=%s&hash=%s' % (self.api_key, self.hash)

        # Выделить аккаунт из ключа API
        try:
            index = api_key.find('_')
            # Проверка на правильность формата ключа
            if index != -1 and len(api_key) > index + 1:
                self.account_id = int(api_key[:api_key.find('_')])
            else:
                raise ValueError()
        except Exception:
            raise RingCloudError('The API key must have the following form: xxx_yyyy, '
                                 'where xxx - account id (integer), and yyyy - hash value.')

    def get_account_balance(self):
        """
        Get account balance.

        Parameters:

        Returns:
            The account balance (float value)

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        return float(self._request('/v1/accounts/%s/balance' % self.account_id, 'GET'))

    def get_phone_number_info(self, phone_number):
        """
        Get phone number info: country, ABC/DEF code, operator, region (the last three only for Russia)

        Parameters:
            phone_number - Phone number. Phone number should be in E.164 format. The standard is:
                           + <CountryCode> <City / AreaCode> <LocalNumber>
                           The country code is 1-3 digits long, while the city / area code
                           and local number length can vary.

        Returns:
            Dictionary with following parameters:
                country - The country to which this phone number belongs
                operator - The name of the operator who owns the phone number (only for Russia)
                region - Country region (only for Russia)
                DEF/ABC - Area code (only for Russia)

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        return self._request('/v1/phone_numbers/%s' % phone_number, 'GET')

    def get_channels(self):
        """
        Get all active channels for account.

        Parameters:

        Returns:
            List of active channels

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        return self._request('/v1/calls/channels', 'GET')

    def get_channel_info(self, channel_name):
        """
        Get channel info.

        Parameters:
            channel_name - Channel name.

        Returns:
            Channel info as a dictionary:
                ConnectedLineNum
                CallerIDNum
                Seconds
                ConnectedLineName
                CallerIDName
                Channel

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        return self._request('/v1/calls/channels/%s' % channel_name, 'GET')

    def originate(self, user, num):
        """
        Originate call.

        Parameters:
            user - Calling user
            num - Called number

        Returns:
            True

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """
        params = {'user': user, 'num': num}

        self._request('/v1/calls', 'POST', params)
        return True

    def get_active_calls(self):
        """
        Get info about active calls

        Parameters:

        Returns:
            List with active calls. Each element contains following data:
                seconds – The total time of the call (dialing time + talk time)
                src – Calling phone number
                dst – Called phone number
                status – `current` in this case

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        return self._request('/v1/calls/active', 'GET')

    def get_complete_calls(self, days=None, num=None):
        """
        Get info about complete calls

        Parameters:
            days - period (in days) for which the data is requested.
                   Value should be in the range from 1 to 7.
                   The parameter may be omitted, in which case it
                   returns the data for 7 days.
            num - phone number. The parameter may be omitted, in which case
                  it returns the data for all of the phone numbers.

        Returns:
            List with complete calls. Each element contains following data:
                status – `complete` in this case
                src – Calling phone number
                direction – Direction of the call. It can take three values:
                            incoming (call from outside)
                            outgoing (call to external number)
                            internal (call between internal numbers)
                call_start_time – The start time of the call
                rec_file – URL-address to download call recording.
                           To download the file paste URL-address into
                           https://api.ringcloud.ru......?api_key=API_KEY&hash=HASH
                           instead of dots. If there is no record in
                           the field will be `None`
                dst – Called phone number
                disposition – The result of the call. It can take values FAILED,
                              NO ANSWER, BUSY, ANSWERED
                duration – The total time of the call (dialing time + talk time)
                call_end_time – The end time of the call

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        data = ''
        if days is not None:
            data += '&days=%s' % days

        if num is not None:
            data += '&num=%s' % num

        return self._request('/v1/calls/complete', 'GET', get_data=data)

    def get_users(self):
        """
        Get all users for account.

        Parameters:

        Returns:
            List of users

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        return self._request('/v1/users', 'GET')

    def get_user_info(self, user):
        """
        Get info about user

        Parameters:
            user - User name

        Returns:
            User info as a dictionary:
                account_id – клиентский номер
                num – внутренний номер пользователя
                user – имя пользователя
                voice_mail_box – состояние VoiceMail Box для данного пользователя.
                                 Может принимать значения on (включен) или off (выключен)
                mail – email пользователя
                password – пароль пользователя
        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        return self._request('/v1/users/%s' % user, 'GET')

    def create_user(self, password, num, email):
        """
        Create a new user.

        Parameters:
            password – user password
            num – The extension number of the form 4хх (extension number
                  must be unique within the account)
            mail – user email

        Returns:
            The name of the created user

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        params = {'password': password, 'num': num, 'mail': email}

        return self._request('/v1/users/create', 'POST', params=params)

    def update_user_password(self, user, new_password):
        """
        Update user password.

        Parameters:
            user - User name
            new_password - New user password

        Returns:
            True

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        params = {'password': new_password}

        self._request('/v1/users/%s/update_password' % user, 'POST', params=params)

        return True

    def update_user_email(self, user, new_email):
        """
        Update user email.

        Parameters:
            user - User name
            new_email - New user email

        Returns:
            True

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        params = {'mail': new_email}

        self._request('/v1/users/%s/update_email' % user, 'POST', params=params)

        return True

    def update_user_extension(self, user, new_extension):
        """
        Update user extension.

        Parameters:
            user - User name
            new_extension - New user extension (of the form 4хх,
                  must be unique within the account)

        Returns:
            True

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        params = {'num': new_extension}
        self._request('/v1/users/%s/update_extension_number' % user, 'POST', params=params)

        return True

    def enable_user_voice_mail_box(self, user):
        """
        Enable user VoiceMail Box.

        Parameters:
            user - User name

        Returns:
            True

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        self._request('/v1/users/%s/voice_mail_box_on' % user, 'POST')

        return True

    def disable_user_voice_mail_box(self, user):
        """
        Disable user VoiceMail Box.

        Parameters:
            user - User name

        Returns:
            True

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        self._request('/v1/users/%s/voice_mail_box_off' % user, 'POST')

        return True

    def get_user_records(self, user):
        """
        Get all user records.

        Parameters:
            user - User name

        Returns:
            List of lists. Each sub-list contains information about the record:
            [file name, recording time].

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        return self._request('/v1/users/%s/records' % user, 'GET')

    def download_record(self, user, record, local_path):
        """
        Download the record of the call.

        Parameters:
            user - User name
            record - Record name
            local_path -Ppath to save file on the local computer

        Returns:
            True

        Raises:
            RingCloudError - HTTP status code != 200 OK
        """

        return self._download_file('/v1/users/%s/records/%s' % (user, record), local_path)

    def _request(self, url, method='GET', params=None, get_data=''):
        if not url.startswith('/'):
            url = '/' + url
        full_url = self.api_endpoint + url + self.auth + get_data

        data = {'params': params}

        try:
            if method == 'POST':
                if params is not None:
                    resp = requests.post(full_url, data=json.dumps(data), timeout=TIMEOUT)
                else:
                    resp = requests.post(full_url, timeout=TIMEOUT)
            elif method == 'GET':
                resp = requests.get(full_url, timeout=TIMEOUT)
            else:
                raise RingCloudError('Unsupported method %s' % method)

        except requests.RequestException as e:  # errors from requests
            raise RuntimeError(e)

        if resp.status_code != 200:
            raise RingCloudError(str(resp.status_code) + '. ' + json.loads(resp.text)['message'])

        return json.loads(resp.text)['data']

    def _download_file(self, url, local_path):
        if not url.startswith('/'):
            url = '/' + url

        full_url = self.api_endpoint + url + self.auth

        try:
            resp = requests.get(full_url, timeout=TIMEOUT)
        except requests.RequestException as e:  # errors from requests
            raise RuntimeError(e)

        if resp.status_code == 404:
            raise RingCloudError('File not found')

        if resp.status_code != 200:
            raise RingCloudError(str(resp.status_code) + '. ' + json.loads(resp.text)['message'])

        with open(local_path, 'wb') as f:
            f.write(resp.content)
            f.close()


if __name__ == '__main__':
    print("RingCloud API Python Libary")
    print("https://api.ringcloud.ru/docs")

