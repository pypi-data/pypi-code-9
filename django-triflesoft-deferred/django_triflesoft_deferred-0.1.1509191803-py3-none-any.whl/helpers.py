from requests import request

from django.core.mail import EmailMessage


class HttpRequest(object):
    def __init__(self, verb, url, parameters=None, headers=None, data=None):
        self.verb = verb
        self.url  = url
        self.parameters = parameters
        self.headers = headers
        self.data = data

    def __call__(self):
        response = request(self.verb, self.url, params=self.parameters, headers=self.headers, data=self.data)
        response.raise_for_status()


class SendEMail(object):
    def __init__(self, message):
        if not isinstance(message, EmailMessage):
            raise TypeError('message must be django.core.mail.EmailMessage')

        self.message = message

    def __call__(self):
        self.message.send()
