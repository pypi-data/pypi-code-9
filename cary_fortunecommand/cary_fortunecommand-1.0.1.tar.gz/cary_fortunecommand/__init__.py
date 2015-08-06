from cary.carycommand import CaryCommand, CaryAction
import random
from subprocess import Popen, PIPE

"""
A rather silly command to use cowsay and fortune to send back
a somewhat random response.

config items
COWSAY_PATH:string path to the cowsay executable
FORTUNE_PATH:string path to the fortune executable
RANDOM_COWS: {short:long} dictionary of cows with description, ie

RANDOM_COWS = dict(
    bunny="bouncing bunny of arcane knowledge",
    default="standard cow of wisdom",
    sheep="fluffy sheep of hubris",
    squirrel="twitchy squirrel of advice"
    )
"""


class FortuneCommand(CaryCommand):

    @property
    def name(self):
        return "fortune"

    @property
    def description(self):
        return "Return a random fortune.  Contents not endorsed."

    @property
    def required_attachments(self):
        return ["none"]

    def _create_action(self, parsed_message):
        return FortuneAction(parsed_message)


class FortuneAction(CaryAction):

    def __init__(self, parsed_message):
        super().__init__(parsed_message)

    def validate_command(self):
        self.command_is_valid = True

    def random_cow(self):
        if 'RANDOM_COWS' in self.config:
            result = random.choice(list(self.config['RANDOM_COWS'].items()))
        else:
            result = ("default", "standard cow of wisdom")
        return result

    def execute_action(self):
        cow = self.random_cow()
        fortune = Popen([self.config["FORTUNE_PATH"],
                         self.config["FORTUNES_PATH"]], stdout=PIPE)
        cowsay = Popen([self.config["COWSAY_PATH"],
                        "-f",
                        cow[0]],
                        stdin=fortune.stdout,
                        stdout=PIPE)
        output = cowsay.communicate()[0].decode('utf-8')
        self._intro_line = "The {0} saith to thee:\n\n".format(
            cow[1])
        self._message_body = output
        self._output_filenames = []

    @property
    def response_subject(self):
        return "Your random fortune"

    @property
    def response_body(self):
        return self._intro_line + self._message_body

    @property
    def response_body_html(self):
        return("<!DOCTYPE html><html><body><h2>{0}</h2>"
               "<pre>{1}</pre></body></html>".format(
                   self._intro_line, self._message_body
                   ))
