from .util import indent


class GradingError(Exception):

    '''Base class for all errors that may occur during grading.'''

    def __init__(self, template, response=None):
        super().__init__(template, response)
        self.template = template
        self.response = response

    def message(self, format='text'):  # @ReservedAssignment
        '''Return a formatted message string for the given error'''

        try:
            method = getattr(self, 'message_' + format)
        except AttributeError:
            raise ValueError('invalid format: %r' % format)
        return method()

    def message_text(self):
        '''Message formatted as plain text'''

        return repr(self)

    def name(self):
        '''Return the error name'''
        return type(self).__name__

    def title(self):
        '''Return the error title'''

        try:
            return self.TITLE
        except AttributeError:
            name = self.name()
            if name.endswith('Error'):
                name = name[:-5]
            chars = [(c if c.islower() else ' ' + c) for c in name]
            return ''.join(chars)


class BuildError(GradingError):

    '''Flags a syntax error in the input code or any kind of error that may
    prevent the code from building correctly.'''


class UnexpectedError(GradingError):

    '''Code terminates with a segfault, uncaught exception, or any other
    non-zero exit code.'''


class TimeExceededError(GradingError):

    '''Code does not terminate until the maximum estipulated runtime is
    reached.'''


class UnusedInputError(GradingError):

    '''Code runs without errors but do not uses all input values expected to
    be used. Do not check if the output values written up to that point are
    correct.'''

    def __init__(self, template, response, unused):
        super().__init__(template, response)
        self.args = self.args + (unused,)
        self.unused = unused

    def message_text(self):
        title = self.title()
        msg = [
            '-' * len(title),
            title,
            '-' * len(title),
            '\nExpected answer:',
            indent(self.template.format('text')),
            '\nObtained:',
            indent(self.response.format('text')),
            '\nThe following inputs were not used when program finished:',
            '    ' + ', '.join(map(str, self.unused))
        ]
        return '\n'.join(msg) + '\n'


class MissingInputError(GradingError):

    '''Program expects a non-existing input value.'''

    def __init__(self, *args):
        if args:
            template, response = args
            super().__init__(template, response)
        else:
            Exception.__init__(self)

    def message_text(self):
        title = self.title()
        msg = [
            '-' * len(title),
            title,
            '-' * len(title),
            '\nExpected answer:',
            indent(self.template.format('text')),
            '\nObtained:',
            indent(self.response.format('text').rstrip() + '  ???\n...'),
            '\nYour program is asking for more inputs than expected',
        ]
        return '\n'.join(msg) + '\n'


#
# Wrong answers
#
class WrongAnswerError(GradingError, ValueError):

    '''Code runs without error, but computes wrong output values.'''

    def message_text(self):
        title = self.title()
        msg = [
            '-' * len(title),
            title,
            '-' * len(title),
            '\nExpected answer:',
            indent(self.template.format('text')),
            '\nObtained:',
            indent(self.response.format('text')),
        ]
        return '\n'.join(msg) + '\n'


class PresentationError(WrongAnswerError):

    '''Code runs without error and probably computes the correct values.
    However it does not format the output correctly.'''


class BadPromptError(WrongAnswerError):
    '''Code that would be 100% correct if the texts in the prompts were
    ignored.'''
