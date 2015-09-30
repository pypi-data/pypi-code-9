import copy
import collections
from decimal import Decimal
from .. import errors
from .io_strings import *


__all__ = ['Example']


class ListLike(collections.Sequence):
    '''Base class for Example and IOTemplate objects'''

    def __init__(self, template, value=1, parsed=None):
        # Fix template vs. parsed list input
        if isinstance(template, list):
            parsed, template = list(template), None
        elif parsed is None:
            parsed = self._parse(template)

        self.template = template
        self._data = list(parsed)
        self.value = Decimal(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = Decimal(value)

    def _parse(self, template):
        raise NotImplementedError

    def __getitem__(self, idx):
        return self._data[idx]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __eq__(self, other):
        return (len(self) == len(other) and
                all(x == y for (x, y) in zip(self, other)))


class Example(ListLike):
    '''An example of input/output/prompt interactions'''

    _loose_match_args = dict(strip=True)

    def __init__(self, template, value=None, feedback='', parsed=None,
                 error=None, validate=True):
        if value is None:
            value = 0 if error else 1
        self.feedback = feedback
        self.error = error
        super().__init__(template, value=value, parsed=parsed)

        # Some consistency checks
        if validate:
            assert self.__has_one_input_per_prompt() or self.is_input

    def _parse(self, template):
        from .io_parser import parse_example
        return parse_example(template)

    #
    # Properties
    #
    @property
    def is_input(self):
        return all(isinstance(x, In) for x in self)

    @property
    def is_output(self):
        return all(isinstance(x, Out) for x in self)

    @property
    def is_prompt(self):
        return all(isinstance(x, Prompt) for x in self)

    @property
    def grade(self):
        return self.value

    #
    # Public API
    #
    def get_inputs(self):
        '''Return a list with all input strings.'''

        return [x for x in self if isinstance(x, In)]

    def get_outputs(self, *, prompts=True, convert=False):
        '''Return a list with all output strings, including prompts.

        If `prompts=False`, skip Prompt strings from output. If
        `convert=True`, convert Prompt strings to Out strings
        '''

        if prompts:
            data = [x for x in self if isinstance(x, (Out, Prompt))]
            if convert:
                data = [Out(x) for x in data]
            return data
        else:
            return [x for x in self if isinstance(x, Out)]

    def get_grade(self):
        '''Returns the grade for the given run'''

        return self.grade

    def get_message(self, format='text'):  # @ReservedAssignment
        '''Return a formatted message for the given run'''

        if self.error:
            return self.error.message(format)

    def loose_match(self, other, strip=False, casefold=False):
        r'''Match two example objects allowing small (but well defined)
        discrepancies. The default behavior is similar to ``self == other``
        but additional parameters may allow specific types of discrepancies.


        Parameters
        ----------

        strip : bool
            If True, ignore all trailing newlines and whitespace for the last
            output value
        casefold : bool
            If True, convert all strings to lowercase before comparison.


        Examples
        --------

        >>> ex1 = Example('x:a; y:b --> ab')
        >>> ex2 = Example('x:a; y:b --> "ab "')

        These two examples are slightly different since the second outputs an
        additional trailing space.

        >>> ex1 == ex2
        False

        >>> ex1.loose_match(ex2, strip=True)
        True
        '''

        A = list(self)
        B = list(other)

        # Apply transformations
        if strip:
            if isinstance(A[-1], Out):
                A[-1] = A[-1].strip()
            if isinstance(B[-1], Out):
                B[-1] = B[-1].strip()
        if casefold:
            A = [x.casefold() for x in A]
            B = [x.casefold() for x in B]

        # Test othe matches
        is_match = A == B

        return is_match

    def with_grades(self, template):
        '''Return a copy of itself with any possible grading errors.'''

        if isinstance(template, str):
            template = Example(template)

        if self.error or self.loose_match(template, **self._loose_match_args):
            new = self.copy()
        else:
            new = self.copy()
            new.value = 0
            new.error = errors.WrongAnswerError(self, template)

        new.template = template
        return new

    def copy(self):
        '''Return a shallow copy of itself'''

        new = copy.copy(self)
        new._data = new._data[:]
        return new

    def format(self, method='text'):
        try:
            method = getattr(self, 'format_' + method)
        except AttributeError:
            raise ValueError('invalid method: %r' % method)
        return method()

    def format_text(self):
        msgs = []
        for x in self:
            if isinstance(x, In):
                msgs.append('< %s >\n' % x)
                # msgs.append('\n')
            elif isinstance(x, Prompt):
                msgs.append(str(x))
            elif isinstance(x, Out):
                msgs.append(str(x) + '\n')
        data = (''.join(msgs)).rstrip()
        return data or '**empty**'

    #
    # Magic methods
    #
    def __repr__(self):
        if self.template is not None:
            return 'Example(%r)' % self.template

        data = list(self)
        optargs = ''
        if self.value != 1:
            optargs += ', value=' + str(self.value)
        if self.feedback:
            optargs += ', feedback=' + repr(self.feedback)
        if self.error:
            optargs += ', error=' + repr(self.error)

        return 'Example(%r%s)' % (data, optargs)

    #
    # Consistency checks
    #
    def __has_one_input_per_prompt(self):
        n_prompts = sum(1 for x in self if isinstance(x, Prompt))
        n_inputs = sum(1 for x in self if isinstance(x, In))
        return n_prompts == n_inputs
