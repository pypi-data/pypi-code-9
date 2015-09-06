
import json

class Message(object):
    def __init__(self, name, command, arguments = dict()):
        self.name = name
        self.command = command
        self.arguments = arguments

    @staticmethod
    def from_str(message):
        try:
            data = json.loads(message)
        except:
            raise

        try:
            name = data['name']
            command = data['command']
            arguments = data['arguments']
        except:
            raise

        return Message(name, command, arguments)

    def __str__(self):
        return json.dumps(dict(name = self.name, command = self.command, arguments = self.arguments))
