import click

class PacemakerError(click.ClickException):
    pass


class NotFound(PacemakerError):
    def show(self, *args, **kwargs):
        self.message = 'Unable to find %s named %s' % (
            self.noun,
            self.message)
        super(NotFound, self).show()


class NodeNotFound(NotFound):
    noun = 'node'


class ResourceNotFound(NotFound):
    noun = 'resource'


class TimeoutError(PacemakerError):
    pass
