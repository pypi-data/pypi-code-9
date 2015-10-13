
class Environment(object):
    REQUIRED_KEYS = ['CRYPT_AES_KEY', 'CRYPT_IMPAY_KEY', 'IMPAY_IV']
    PREFERRED_KEYS = ['CPCODE', 'CERTTYPE']

    def __init__(self, **kwargs):
        for key in self.REQUIRED_KEYS + self.PREFERRED_KEYS:
            setattr(self, key, kwargs.get(key, None))

    def validate(self):
        for key in self.REQUIRED_KEYS:
            if getattr(self, key) is None:
                raise ValueError(
                    'key {} is expected but not found.'.format(key))
        return True


default = Environment()
