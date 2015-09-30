'''
In, Out, and Prompt strings for Example objects.
'''

import collections

__all__ = ['In', 'Out', 'Prompt']


class ParsedString(collections.UserString):

    '''Strings that appear in the parsed output'''

    is_input = False
    is_output = False
    is_prompt = False

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, str(self))

    def render(self):
        '''Return a string representation of the token'''

        return str(self)


class In(ParsedString):

    '''Represent input strings in an example interaction.'''

    is_input = True


class Out(ParsedString):

    '''Represent output strings in an example interaction.'''

    is_output = True


class Prompt(Out):

    '''Represent a string that is shown when asking the user for some input.
    The grader may interpret these strings as optional.'''

    is_prompt = True
