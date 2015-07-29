import contextlib
import collections
import time

from boto.exception import BotoServerError
from retrying import retry


@retry(retry_on_exception=lambda e: isinstance(e, BotoServerError),
       wait_exponential_multiplier=1000,
       wait_exponential_max=10000)
def cfn_retry(op):
    return op()


class Stack(object):
    def __init__(self, cfn_stack):
        """
        Creates a nicer representation of a boto.cloudformation.stack.Stack.
        """
        self.stack_id = cfn_stack.stack_id
        self.stack_name = cfn_stack.stack_name
        self.outputs = {o.key: o.value for o in cfn_stack.outputs}
        self.tags = cfn_stack.tags


class Resolver(object):
    def __init__(self, cfn, strategy, filters):
        self.cfn = cfn
        self.strategy = strategy
        self.filters = filters
        self.cache = collections.defaultdict(dict)

    def __call__(self, name, output):
        if name in self.cache:
            stacks = self.cache[name].values()
        else:
            stacks = self.strategy(self.cfn, name)

        for stack in stacks:
            # strategy may yield many stacks with same name
            self.cache[name][stack.stack_id] = stack

            all_filters_match = all(
                item in stack.tags.items()
                for item in self.filters.items()
            )
            if all_filters_match and output in stack.outputs:
                # return first match, ignoring any other possible matches
                return stack.outputs[output]

        raise ResolutionError(name, output)


def ResolveByName(cfn, name):
    """
    Resolution strategy which will match stacks against their stack name.
    """
    next_token = None
    keep_listing = True

    while keep_listing:
        # Use list stacks which is more efficient than describe_stacks
        # when a name is not specified
        resp = cfn_retry(lambda: cfn.describe_stacks(name, next_token))
        for stack in resp:
            yield Stack(stack)

        next_token = resp.next_token
        keep_listing = next_token is not None

    raise StopIteration


class ResolveByTag(object):
    """
    Resolution strategy which will match stacks against the value of the tag
    provided.
    """

    valid_states = [
        'CREATE_COMPLETE',
        'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
        'UPDATE_COMPLETE',
        'UPDATE_ROLLBACK_COMPLETE'
    ]

    def __init__(self, tag):
        self.tag = tag

    def __call__(self, cfn, name):
        next_token = None
        keep_listing = True

        while keep_listing:
            # Use list stacks which is more efficient than describe_stacks
            # when a name is not specified
            resp = cfn_retry(
                lambda: cfn.list_stacks(self.valid_states, next_token)
            )
            for summary in resp:
                # Lookup the full stack details
                stack = cfn_retry(
                    lambda: cfn.describe_stacks(summary.stack_id)
                )
                s = Stack(stack[0])
                if s.tags.get(self.tag) == name:
                    yield s

            next_token = resp.next_token
            keep_listing = next_token is not None

        raise StopIteration


class ResolutionError(Exception):
    def __init__(self, stack, output):
        self.stack = stack
        self.output = output

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return (
            'Could not resolve output "{}" from stack "{}"'
            .format(self.output, self.stack)
        )
