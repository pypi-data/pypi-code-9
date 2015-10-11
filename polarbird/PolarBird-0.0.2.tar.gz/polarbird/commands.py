import twitter

from polarbird.printers import (
    print_tweet, print_retweet, print_twitter_error, colorize
)
from polarbird.colors import colors

class CommandLine(object):
    """
    Command line handler for commands from user
    """

    def __init__(self, app):
        self._app = app
        self._commands = {}
        self._register_commands()

    def listen(self):
        """
        Listen method for user input
        """
        while True:
            user_input = input(colors['reset'] + '>> ')
            if user_input and user_input[0] == '/':
                self._handle_command(user_input)
            elif user_input:
                print(colorize('\'{}\''.format(user_input), colors['reset']))
                confirmation = input(colorize(
                    'Are you sure to send the tweet (yes/no)? ', colors['reset']
                ))
                if confirmation == 'yes':
                    self._send_tweet(user_input)

    def _get_twitter(self):
        """
        Getting Twitter instance to access API.
        """
        tw = twitter.Twitter(auth=self._app.auth)

        return tw

    def _register_commands(self):
        """
        Register command classes for use in command line.
        """
        commands_cls = (HomeCommand, RetweetCommand,)
        for cls in commands_cls:
            cmd = cls(self)
            self._commands[cmd.NAME] = cmd

    def _handle_command(self, command):
        """
        Handle command which starts with '/'.
        """
        cmd_and_args = command[1:].split(' ')
        if cmd_and_args[0] == 'exit':
            exit(0)
        elif cmd_and_args[0] == 'help':
            try:
                self._show_help(cmd_and_args[1])
            except IndexError:
                self._show_full_help()
        elif cmd_and_args[0] in self._commands:
            tw = self._get_twitter()
            try:
                self._commands[cmd_and_args[0]].execute(tw, cmd_and_args[1])
            except twitter.TwitterHTTPError as e:
                print_twitter_error(e)
            except IndexError:
                self._commands[cmd_and_args[0]].execute(tw)

    def _send_tweet(self, text):
        """
        Send new tweet if message is lesser or equal to 140 characters.
        """
        t = self._get_twitter()
        try:
            t.statuses.update(status=text)
        except twitter.TwitterHTTPError as e:
            print_twitter_error(e)

    def _show_help(self, cmd):
        """
        Show help for specified command.
        """
        if cmd in self._commands:
            print(self._commands[cmd].HELP_TEXT)

    def _show_full_help(self):
        """
        Show complete help page with all available commands.
        """
        builtin_commands = ['help', 'exit']
        print('List of available commands: {commands}'.format(
            commands=', '.join(list(self._commands.keys()) + builtin_commands)
        ))

class Command(object):
    """
    Base class for every command
    """

    NAME = None
    HELP_TEXT = None

    def __init__(self, command_line):
        if not self.NAME:
            raise ValueError(
                'NAME is not set for class {!r}'.format(self.__class__.__name__)
            )
        if not self.HELP_TEXT:
            raise ValueError(
                'HELP_TEXT is not set for class {!r}'.format(self.__class__.__name__)
            )
        self._command_line = command_line

    def execute(self, t, args=None):
        raise NotImplementedError

class HomeCommand(Command):
    """
    Home command for home timeline view
    """

    NAME = 'home'
    HELP_TEXT = 'Shows home timeline for current logged user.'

    def execute(self, t, args=None):
        tweets = t.statuses.home_timeline()
        for tweet in reversed(tweets):
            key = self._command_line._app.tweet_database.insert(tweet)
            if 'retweeted_status' in tweet:
                print_retweet(tweet, key)
            else:
                print_tweet(tweet, key)

class RetweetCommand(Command):
    """
    Command for retweeting based on Tweet index from TweetDatabase
    """

    NAME = 'rt'
    HELP_TEXT = 'Retweet a tweet.'

    def execute(self, t, args=None):
        if not args:
            print(colorize(
                'You have to specify tweet ID to retweet.', colors['yellow']
            ))
        else:
            self._retweet(t, args)

    def _retweet(self, t, args):
        try:
            tweet_id = self._command_line._app.tweet_database[args]['id']
            t.statuses.retweet(id=tweet_id, include_entities=False, trim_user=True)
        except KeyError:
            print(colorize('Invalid tweet index.', colors['yellow']))
