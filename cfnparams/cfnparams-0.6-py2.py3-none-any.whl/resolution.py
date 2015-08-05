import collections

from boto.exception import BotoServerError
from retrying import retry

import cfnparams.exceptions


def with_retry(cls, methods):
    """
    Wraps the given list of methods in a class with an exponential-back
    retry mechanism.
    """
    retry_with_backoff = retry(
        retry_on_exception=lambda e: isinstance(e, BotoServerError),
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000
    )
    for method in methods:
        m = getattr(cls, method, None)
        if isinstance(m, collections.Callable):
            setattr(cls, method, retry_with_backoff(m))
    return cls


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
        self.cfn = with_retry(cfn, ['list_stacks', 'describe_stacks'])
        self.strategy = strategy
        self.filters = filters

    def __call__(self, name, output):
        for stack in self.strategy(self.cfn, name):
            all_filters_match = all(
                item in stack.tags.items()
                for item in self.filters.items()
            )
            contains_output = output in stack.outputs
            if all_filters_match and contains_output:
                # return first match, ignoring any other possible matches
                return stack.outputs[output]

        raise cfnparams.exceptions.ResolutionError(name, output)


class ResolveByName(object):
    """
    Resolution strategy which will match stacks against their stack name.
    """

    def __init__(self):
        self.cache = collections.defaultdict(dict)

    def __call__(self, cfn, name):
        if name in self.cache:
            for stack in self.cache[name].values():
                yield stack
        else:
            next_token = None
            keep_listing = True

            while keep_listing:
                # Use list stacks which is more efficient than describe_stacks
                # when a name is not specified
                resp = cfn.describe_stacks(name, next_token)
                for summary in resp:
                    stack = Stack(summary)
                    self.cache[name][stack.stack_id]
                    yield stack

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
        self.cache = collections.defaultdict(dict)

    def __call__(self, cfn, name):
        # Optimistically serve stack from cache
        if name in self.cache:
            for stack in self.cache[name].values():
                yield stack

        # Maybe it's not in the cache yet? Walk through the full list again
        next_token = None
        keep_listing = True

        while keep_listing:
            # Use list stacks which is more efficient than describe_stacks
            # when a name is not specified
            resp = cfn.list_stacks(self.valid_states, next_token)
            for summary in resp:
                # Already yielded this stack, skip it
                if summary.stack_id in self.cache[name]:
                    continue

                # Lookup the full stack details
                stack = cfn.describe_stacks(summary.stack_id)
                s = Stack(stack[0])
                self.cache[name][s.stack_id] = s
                if s.tags.get(self.tag) == name:
                    yield s

            next_token = resp.next_token
            keep_listing = next_token is not None

        raise StopIteration
