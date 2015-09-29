from __future__ import print_function

import sys


def write_to_file_and_stream(command, outstream, outfile):
    if outstream:
        print(command, file=sys.stderr)

    with open(outfile, "a") as handle:
        outstr = create_print_and_execute_string(command)
        handle.write(outstr)



def create_print_and_execute_string(command):

    proper_quote_symbol = opposite_quotesymbol(command)

    template = """print({quote}{command}{quote})"""
    print_string = template.format(quote=proper_quote_symbol,
                                    command=command)
    return "\n".join([print_string, command, "\n"])


def opposite_quotesymbol(command):

    if "'" not in command and '"' not in command:
        # if there are no quotesymbols in the command, use whichever
        return '"'

    opposite_quotes = {'"': "'", "'": '"'}

    quotes_only = [c for c in command if c in opposite_quotes]

    first_quote, last_quote = quotes_only[0], quotes_only[-1]
    assert first_quote == last_quote, \
        "Mismatched quote symbols in: {}".format(command)

    return opposite_quotes[first_quote]
