from time import time

from bst.pygasus.core import ext
from bst.pygasus.session.interfaces import ISession
from bst.pygasus.session.interfaces import IClientIdentification
from bst.pygasus.session.interfaces import DEFAULT_EXPIRATION


class UserSessionData(dict):

    def __init__(self):
        self.reset_lastchanged()

    def reset_lastchanged(self):
        self.lastchanged = time()


class RamSessionData(dict):
    def __init__(self, expiration=None):
        if expiration is None:
            expiration = DEFAULT_EXPIRATION
        self.expiration = expiration
ram = RamSessionData()


class RamSession(ext.Adapter):
    """ simple session thats store data unencrypted in ram. After shutdown
        the server all data will lost.
        For a persistent session class you properly should
        inherit from this class.
    """
    ext.implements(ISession)
    ext.context(ext.IRequest)

    user_session_data_cls = UserSessionData

    def __init__(self, request):
        self.request = request

    def __setitem__(self, key, value):
        client = IClientIdentification(self.request)
        identification = client.identification()
        if identification is None or identification not in self.store():
            identification = client.apply()
        data = self.store().setdefault(identification, self.user_session_data_cls())
        data[key] = self.encrypt(value)
        data.reset_lastchanged()

    def __getitem__(self, key):
        self.refresh()
        identification = IClientIdentification(self.request).identification()
        if identification is None or identification not in self.store():
            raise KeyError('user has no identification or data')
        return self.decrypt(self.store()[identification][key])

    def __delitem__(self, key):
        identification = IClientIdentification(self.request).identification()
        if identification is None or identification not in self.store():
            raise KeyError('user has no identification or data')
        del self.store()[identification]

    def __contains__(self, key):
        identification = IClientIdentification(self.request).identification()
        if identification is None:
            return False
        if identification not in self.store():
            return False
        return key in self.store()[identification]

    def set_expiration_time(self, time):
        self.store().expiration = time

    def get_expiration_time(self):
        return self.store().expiration

    def store(self):
        """ return a store in form of a dict
        """
        return ram

    def decrypt(self, value):
        """ this function do nothing but
            can easily overridden in a subclass
        """
        return value

    def encrypt(self, value):
        """ this function do nothing but
            can easily overridden in a subclass
        """
        return value

    def refresh(self):
        removes = list()
        for key, data in self.store().items():
            if data.lastchanged + self.get_expiration_time() < time():
                removes.append(key)
        for key in removes:
            del self.store()[key]
