class _Command(object):

    def __init__(self, *args, **kwargs):
        self.args = args or []
        self.kwargs = kwargs or {}

    def execute(self):
        return self.callback()

    def callback(self):
        pass


class _Chain(object):

    def __init__(self):
        self.commands = []

    def add(self, command):
        self.commands.append(command)

    def run(self):
        for command in self.commands:
            result = command.execute()
            if result is not None:
                return result
