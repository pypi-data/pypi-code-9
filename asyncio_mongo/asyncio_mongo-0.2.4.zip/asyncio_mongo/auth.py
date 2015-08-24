import asyncio


class Authenticator:

    def authenticate(self, db):
        raise NotImplementedError()


class CredentialsAuthenticator():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @asyncio.coroutine
    def authenticate(self, db):
        yield from db.authenticate(self.username, self.password)