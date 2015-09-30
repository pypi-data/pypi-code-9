'''IO questions templates specify a sequence of input/output pairs expected
to appear in a given program. It is a simple language that is parsed into a
sequence of Example() sequences that are suitable to be used as a list of
examples by an automated grades. Optionally, the user may specify the input
strings and a program that compute the responses as output strings.

Template language
-----------------

The most simple construct is the input/output pair given bellow::

    "input prompt": "input string" --> "output string"

The quotes are optional, but may be necessary to escape special character
sequeces such as ":", "-->", etc, or to have a precise control of whitespace.
Consecutive lines are interpreted as a sequence of interations whithin a single
execution. Use a blank line to separate different executions. Comments start
with "#".

::
    # First example: sum two floats
    "x: ": "1.0";
    "y: ": "2.0";
    --> "sum = 3.0"

    # Second example: sum two ints
    "x: ": "1";
    "y: ": "2";
    --> "sum = 3.0"

Since the colon character ``:`` often appears in input prompts, we created the
following shortcuts: ``x::y`` is translated to ``"x:": "y"`` and ``x:: y`` is
translated to ``"x: ": "y"``. This allows some compact representations such
as::

    # sum two floats
    x:: 1.0; y:: 2.0 --> sum = 3.0

    # sum two ints
    x:: 1; y:: 2 --> sum = 3.0

Multiline output strings can be specified by a heading ``|`` in the beginning
of each line

::
    x:: a; y:: b;
    -->
        |multiline output
        |another line
        |another line

Indentation is optional but helps with readability.


If only input strings are specified, the grader may compute the complete
interaction from an example program which represent a correct answer. In this
case, just list inputs as a sequence of strings followed by semi-colons::

    1; 2; 3; 4;

New lines and other forms of whitespace are not important.

Each block of examples can start with a parenthesized argument list that
specify some options to the grader. The grader accept two optional parameters
as in the example::

    # sum two ints
    x:: 1; y:: 2 --> sum = 3.0

    # An argument modifying a single example
    [ 50%, output must display a least a decimal place ]
    x:: 1; y:: 2 --> sum = 3

    # An argument modifying multiples examples
    [ 75%, output must have the same number of decimal places as the input ]
        x:: 1.25; y:: 1.25 --> sum = 2.50

        x:: 1.250; y:: 1.25 --> sum = 2.500

        x:: 1.25; y:: 1.250 --> sum = 2.500


Configuration options
---------------------


Parsed output
-------------

...
'''

import re
from . import In, Out, Prompt, Example, IOTemplate

__all__ = ['parse_io_template']


def parse_io_template(template):
    '''Parse the template string into a parsed list of examples.

    Example
    -------

    >>> parse_io_template('x:a; y:b --> ab')
    IOTemplate([Example('x:a; y:b --> ab')])

    Each example consists of a list of input/output/prompt strings

    >>> example = parse_io_template('x:a; y:b --> ab')[0]
    >>> list(example)
    [Prompt('x'), In('a'), Prompt('y'), In('b'), Out('ab')]
    '''

    template = '\n'.join([line.strip() for line in template.splitlines()])
    examples = [line.strip() for line in template.split('\n\n') if line]
    examples = [parse_example(example) for example in examples]
    return IOTemplate([x for x in examples if x is not None])


def parse_example(template):
    '''Parse a string for a single example'''

    tk_list = tokenizer(template)

    # Join string lists
    while True:
        try:
            idx = tk_match_seq(tk_list, String, Whitespace, String)
            st = tk_list[idx][Example('x:a; y:b --> ab')]
            st += tk_list.pop(idx + 1)
            st += tk_list.pop(idx + 1)
            tk_list[idx] = String(st)
        except ValueError:
            break

    # Strip comments and whitespace
    tk_list = [tk for tk in tk_list if not isinstance(tk, Comment)]
    tk_list = [tk for tk in tk_list if not isinstance(tk, Whitespace)]

    # Return an empty template
    if not tk_list:
        return None

    while isinstance(tk_list[0], (Paragraph, NewLine)):
        del tk_list[0]
    while isinstance(tk_list[-1], (Paragraph, NewLine)):
        tk_list.pop()

    # Convert multiline strings
    for idx, tk in enumerate(tk_list):
        if isinstance(tk, MultiLine):
            data = ''
            for line in tk[1:-1].splitlines():
                data += line.partition('|')[-1] + '\n'
            tk_list[idx] = String(data[:-1])

    # Match foo:: bar and convert to "foo: ": bar
    while True:
        try:
            idx = tk_match_seq(tk_list, String, (':: ', '::'), String)
            sep = tk_list[idx + 1]
            tk_list[idx] = String(tk_list[idx] + sep[1:])
            tk_list[idx + 1] = Colon(':')
        except ValueError:
            break

    # Match all arrows and insert output
    while True:
        try:
            idx = tk_match_seq(tk_list, Arrow, String, (NewLine, SemiColon))
            tk_list.pop(idx + 2)
        except ValueError:
            break

    while True:
        try:
            idx = tk_match_seq(tk_list, Arrow, String)
            data = tk_list.pop(idx + 1)
            tk_list[idx] = Out(data)
        except ValueError:
            break

    # Match all colon definitions
    while True:
        try:
            idx = tk_match_seq(tk_list, String, Colon, String)
            in_ = In(tk_list.pop(idx + 2))
            out = Prompt(tk_list[idx])
            tk_list[idx] = out
            tk_list[idx + 1] = in_
        except ValueError:
            break

    # Match all String/semicolon combinations
    while True:
        try:
            idx = tk_match_seq(tk_list, String, (NewLine, SemiColon))
            data = tk_list.pop(idx)
            tk_list[idx] = In(data)
        except ValueError:
            break

    # Match all input_str/semicolon combinations
    while True:
        try:
            idx = tk_match_seq(tk_list, In, (NewLine, SemiColon))
            tk_list.pop(idx + 1)
        except ValueError:
            break

    if isinstance(tk_list[0], Args):
        args, tk_list = tk_list[0], tk_list[1:]
        args, kwargs = args
        kwargs['parsed'] = tk_list
        return Example(template, *args, **kwargs)
    return Example(template, parsed=tk_list)


#
# Input stream tokenizer
#
class Token(str):

    '''Base class for all tokenizer in the input stream'''

    def __repr__(self):
        tname = type(self).__name__
        return '%s(%s)' % (tname, super().__repr__())


class Whitespace(Token):
    regex = re.compile(r'[ \t]+')


class String(Token):
    regex = re.compile(r'''("[^"\n]*"|'[^'\n]*')''')


class Colon(Token):
    regex = re.compile(r'(:: |::|:)')


class SemiColon(Token):
    regex = re.compile(r';')


class NewLine(Token):
    regex = re.compile(r'(\r\n|\n)')


class Arrow(Token):
    regex = re.compile(r'-->')


class MultiLine(Token):
    regex = re.compile(r'(\n[ ]+[|][^\n]*)+')


class Comment(Token):
    regex = re.compile(r'#[^\n]*\n')


class Paragraph(Token):
    regex = re.compile(r'([ \t]*(\r\n|\n))+')


TK_CLASSES = [Whitespace, String, Colon, SemiColon, NewLine, Arrow, MultiLine,
              Comment, Paragraph]
REGEX_PAIRS = [(cls.regex, cls) for cls in TK_CLASSES]
REGEX_MAP = dict(REGEX_PAIRS)
REGEX_LIST = [x for (x, y) in REGEX_PAIRS]

#
# Utility functions
#


def tokenizer(template, out=None):
    '''Return a string of tokens from the given input template string.'''

    out = [] if out is None else out
    if not template.endswith('\n'):
        template += '\n'

    while template:
        # Match any regex expression
        matches = [re.search(template) for re in REGEX_LIST]
        matches = [(m.start(), m.end(), m) for m in matches if m is not None]
        if any(matches):
            # Group by lowest starting index
            matches.sort(key=lambda x: x[0])
            lowest = matches[0][0]
            matches = [(j, m) for (i, j, m) in matches if i == lowest]

            # Find largest match in group
            matches.sort(key=lambda x: x[0], reverse=True)
            highest, match = matches[0]

            # Extract match, data, etc
            pre = template[:lowest]
            data = template[lowest:highest]
            template = template[highest:]

            # Process string tokenizer
            if match.re is String.regex:
                data = data[1:-1]

            # Check if pre has invalid characters
            # ...
            if pre:
                out.append(String(pre))
            out.append(REGEX_MAP[match.re](data))
            continue

        template = out.append(template)

    return out


def tk_match(value, arg):
    '''Matches value with argument either by type (e.g.:
    ``isinstance(value, arg)``), or by value (e.g.: ``value == arg``)'''

    if isinstance(arg, type):
        return isinstance(value, arg)
    else:
        return arg == value


def tk_match_seq(L, *args, raises=True):
    '''Return the index of the first token at a sequence that matches each of
    the given extra arguments::


    tk_match_seq(L, String, '::', String) --> the first ocurrence of tokens
    that matches each of the given arguments in order.
    '''

    n = len(L) - len(args) + 1
    for i, x in enumerate(L[:n]):
        for j, arg in enumerate(args):
            value = L[i + j]
            if not isinstance(arg, (tuple, list)):
                arg = (arg,)
            if not any(tk_match(value, x) for x in arg):
                break
        else:
            return i

    if raises:
        raise ValueError
    else:
        return -1


def tk_split(tk_list, sep):
    '''Split token list in the ``head, sep, tail`` parts.'''

    if isinstance(sep, type):
        def split(x):
            return isinstance(x, sep)
    else:
        def split(x):
            return x == sep

    group = []
    groups = [group]

    for tk in tk_list:
        if split(tk):
            group = []
            groups.append(group)
        else:
            group.append(tk)
    return groups


class Args(object):
    '''Represent the arguments passed to the example constructor.'''

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        yield self.args
        yield self.kwargs


if __name__ == '__main__':
    f1 = '''
    # foo
    x:y;x:y-->bar

    x: y; x:y --> bar
    x:y --> foo
    '''

    f2 = 'foo x: y --> bar'

    f3 = '''foo:: 3
    -->
        |foo
        |bar
        |    foobar'''

    f4 = '-->"hello world"'
    f = f1

    print(parse_io_template(f))

    import doctest
    doctest.testmod()
