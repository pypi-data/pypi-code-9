class AuthorizationException(Exception):
    """Raised when authorization verification failed.
       Contains details about the authentication rules that have been checked.
    """

    def __init__(self, msg):
        self.msg = msg
        super().__init__()

    def __str__(self):
        return 'authorization failed: {}'.format(self.msg)
