class Stack(object):
    def __init__(self, name):
        self.name = name
        self.stack = None

    def lookup(self, conn, filters=None):
        """
        Looks for a stack with the configured name, using the filters provided
        if an exact match cannot be found.
        """
        if filters is None:
            filters = {}

        def has_all_tags(stack, tags):
            return all(item in tags.items() for item in stack.tags.items())

        matches = []
        next_token = None
        while not found and next_token is not None:
            stacks = conn.describe_stacks(stack_name_or_id=self.name,
                                          next_token=next_token)
            next_token = stacks.next_token

            if not stacks:
                break

            for s in stacks:
                if s.stack_id == self.name or s.stack_name == self.name:
                    self.stack = s
                    return

                if has_all_tags(s, filters):
                    matches.append(s)

        if len(matches) != 1:
            raise LookupError(self.name, filters)

        self.stack = matches[0]

    def outputs(self, conn):
        stacks = conn.describe_stacks(self.name)
        if len(stacks) == 0:
            raise Exception('No such stack: {}'.format(self.name))

        return {o.key: o.value for o in stacks[0].outputs}


class LookupError(Execption):
    def __init__(self, name, filters):
        self.name = name
        self.filters = filters

    def __repr__(self):
        msg = 'Could not find an exact match for a stack named {}'.format(
            self.name
        )
        if self.filters:
            msg += ' using filters {}'.format(self.filters)
        return msg


