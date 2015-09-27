import subprocess

__version__ = '0.1.0'


class AuthenticationError(Exception):
    def __init__(self, cause):
        super(AuthenticationError, self).__init__()
        self.cause = cause


def get_token(ssh):
    try:
        return subprocess.check_output('ssh -T {}'.format(ssh), shell=True).strip()
    except subprocess.CalledProcessError as e:
        raise AuthenticationError(e)
