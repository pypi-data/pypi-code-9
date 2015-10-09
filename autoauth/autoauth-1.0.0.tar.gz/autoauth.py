'''authentication in urllib2 and requests for the command line'''

from __future__ import print_function
import base64
import sys
import getpass


try:
    raw_input
except NameError:
    raw_input = input


class Authenticate(object):
    def __init__(self, application, username=None, password=None):
        self.application = application
        self.username = username
        self.password = password

    @property
    def credentials(self):
        if self.username is None or self.password is None:
            return None
        return (self.username, self.password)

    def load_password(self):
        try:
            import keyring
        except ImportError:
            print("keyring module not found", file=sys.stderr)
            raise KeyError(self.username)

        password = keyring.get_password(self.application,
                                        self.username)

        if password is None:
            raise KeyError(self.username)

        self.password = password

    def save_password(self):
        try:
            import keyring
        except ImportError:
            return

        keyring.set_password(self.appliaction,
                             self.username,
                             self.password)

    def get_credentials(self):
        if self.username is None:
            if not sys.__stdin__.isatty():
                raise Exception("Need a username, but stdin is not interactive")
            self.username = raw_input('Username: ')

        if self.password is None:
            try:
                self.load_password()
            except KeyError as e:
                password = getpass.getpass('Password: ')
                if password != '':
                    self.password = password
                    self.save_password()

        return self.credentials

    def on_request(self, request):
        if self.credentials is None:
            self.get_credentials()
        encode = base64.b64encode(("%s:%s" % self.credentials).encode('utf-8'))
        request.headers['Authorization'] = 'Basic %s' % encode

    # alias for requests
    __call__ = on_request


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('application')
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()
    auth = Authenticate(args.application, args.username, args.password)

    credentials = auth.get_credentials()
    if credentials is None:
        sys.exit(1)
    print('%s\t%s' % credentials)
