
def check_command(command_string):

    if unbalanced(command_string):
        e_s = "Unmatched paranthesis or quote in {}. Unable to continue." \
            .format(command_string)
        raise IllegalRCommandException(e_s)

class IllegalRCommandException(Exception):
    pass

def unbalanced(line):
    """
    Check that the command string does not contain unmatched parens or other
    quotes.

    Thanks to Maria Zverina at SO.
    """

    iparens = iter('''""()''{}[]<>''')
    parens = dict(zip(iparens, iparens))

    syms = [x for x in line if x in '\'"[]()']
    stack = []
    for s in syms:
        try:
            if len(stack) > 0 and s == parens[stack[-1]]:
                stack.pop()
            else:
                stack.append(s)
        except: # catches stack underflow or closing symbol lookup
            return True

    return len(stack) != 0
