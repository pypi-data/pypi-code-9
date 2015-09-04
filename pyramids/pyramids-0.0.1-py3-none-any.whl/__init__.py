#!/usr/bin/env python

"""
Pyramids
========
A semantic natural language parser for English.
Copyright (c) Aaron Hosford 2011-2015

Pyramids gets its name from how it constructs parse trees, working upwards
from the leaves towards the root, building up layers of progressively
smaller size but greater scope. It is a rule-based natural language parser,
tailored specifically for English, which builds multiple competing parses
for a sentence from the bottom up using principles of dynamic programming.
The parses are then scored for quality and presented in order of descending
rank. The parser is also capable of accepting feedback as to which parses
are or are not acceptable, adaptively adjusting its scoring measures to
improve future parse quality and ranking. Parses are returned as trees but
can also be used to generate graphs representing the semantic relationships
between words. The syntactic rules of the parser can also be run in reverse
to generate sentences from semantic graphs resembling those it produces.
"""

# =========================================================================
# Modification History:
#
#   7/14/2011:
#     - Created this module using basic_parser.py as a template.
#   8/4/2015:
#     - Python 2.7 => Python 3.4
#
# =========================================================================


# TODO: Factor complexity costs into parse scores; the further a parse tree
#       is from the ideal depth, the worse it fares.

# TODO: Add in stopping conditions, so that if a full-coverage tree has
#       lower average score than a forest of sentences that together cover
#       the same text, the forest of sentences is used instead.

# TODO: Handle emergency parsing by ignoring properties when the best
#       parse's score is sufficiently terrible or no full-coverage tree is
#       found.

# TODO: Add a precedence system to the grammar, allowing us to indicate
#       just how desperate the parser has to be before it even tries a
#       particular rule. Then we can implement the above TODO by having
#       property-free versions automatically generated for each rule, with
#       last-ditch priority. It should also significantly reduce parsing
#       time for certain situations if we make less common usage have
#       slightly lower precedence, by avoiding checking those rules if they
#       aren't worth it. Another option would be to have a score-based
#       cutoff in the parsing routine which disregards potential parse
#       trees & stops early if a full- coverage parse has been found and
#       that parse's score is way higher than all the partial trees left to
#       be considered. Or it could compare the score of each new parse tree
#       to be considered against its direct competitors instead of the
#       parse as a whole, so we save time even when a parse fails.

# TODO: Where should the data folder go? Is it in the standard place?


from pyramids.control import ParserCmd

__author__ = 'Aaron Hosford'
__version__ = '0.0.1'


def main():
    parser_cmd = ParserCmd()
    print('')
    parser_cmd.cmdloop()


if __name__ == "__main__":
    main()
