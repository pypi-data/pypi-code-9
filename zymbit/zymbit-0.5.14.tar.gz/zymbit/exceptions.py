class CommandError(Exception):
    pass


class ConnectionError(Exception):
    pass


class NotConnected(Exception):
    pass


class ProvisionError(Exception):
    pass


class TasksFailed(Exception):
    pass


class TunnelError(Exception):
    pass
