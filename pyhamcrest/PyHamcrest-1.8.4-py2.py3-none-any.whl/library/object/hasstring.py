from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

__author__ = "Jon Reid"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"


class HasString(BaseMatcher):

    def __init__(self, str_matcher):
        self.str_matcher = str_matcher

    def _matches(self, item):
        return self.str_matcher.matches(str(item))

    def describe_to(self, description):
        description.append_text('an object with str ')          \
                    .append_description_of(self.str_matcher)


def has_string(match):
    """Matches if ``str(item)`` satisfies a given matcher.

    :param match: The matcher to satisfy, or an expected value for
        :py:func:`~hamcrest.core.core.isequal.equal_to` matching.

    This matcher invokes the :py:func:`str` function on the evaluated object to
    get its length, passing the result to a given matcher for evaluation. If
    the ``match`` argument is not a matcher, it is implicitly wrapped in an
    :py:func:`~hamcrest.core.core.isequal.equal_to` matcher to check for
    equality.

    Examples::

        has_string(starts_with('foo'))
        has_string('bar')

    """
    return HasString(wrap_matcher(match))
