#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = '''10 Digit Phone Numbers Question

Given a standard phone with the number keys arranged as follows:

1 2 3
4 5 6
7 8 9
* 0 #

Calculate the number of unique 10 digit phone numbers that can be created with the conditions that you may start at any
digit and can repeat a digit as often as you like but you may only change digits by moving diagonally (in any direction).

For instance if you are on the digit 1 the only allowable move is to 5, if you are on 6 the allowable moves would be to
2 and 8.

Once you have moved to a new digit you must dial the new digit at least once. So although 9 is along a diagonal from 1
phone numbers that contain 1 9 are NOT considered valid. Phone numbers that contain 1 5 9 are considered valid.

The * and # are not considered digits and are not part of any valid phone numbers.

The following are valid phone numbers:
1 1 1 1 1 1 1 1 1 1
9 5 1 5 1 1 5 9 5 9

The following are NOT valid phone numbers
1 2 3 4 5 6 7 8 9 0
1 9 9 9 9 9 9 9 9 9

Please write a progam in the language of your choice to solve the above problem. Submit all source files and any test
cases or input files that you use in solving this problem within the allotted time. Late submissions will not be
accepted.

Please remember that you solution will be evaluated on correctness, efficiency and the design of the code written to
solve the problem. A good solution should be both correct and easily readable by persons other than the original author.
Please use readable naming conventions and modular code design in your solution.

Although this problem considers only the standard 10 digit keypad and a fixed set of rules for constructing phone
numbers your code should be designed in a way such that it could be very easily extended to handle different keypads
or different rules for valid phone numbers.
'''


class Motif(object):
    """ A class for motif's question
    """

    def __init__(self):
        # current digit map to number of next possible digits
        self.NUM_OF_POSSIBLE_NEXT_DIGIT = {
            0: 3, 1: 2, 2: 3, 3: 2, 4: 3, 5: 5, 6: 3, 7: 3, 8: 3, 9: 3}

        # current digit map to next possible digit
        self.DIGIT_MAP = {0: (0, 7, 9),
                          1: (1, 5),
                          2: (2, 4, 6),
                          3: (3, 5),
                          4: (2, 4, 8),
                          5: (1, 3, 7, 9, 5),
                          6: (6, 2, 8),
                          7: (7, 5, 0),
                          8: (8, 4, 6),
                          9: (9, 5, 0)}

    def run(self, phone_number_length):
        """ iteratively calculate the possible number of unique phone_number_length digit phone numbers

        :parameter
            digit_number - int, the length of phone number (10 in the question)

        :return
            the number of all permutations of phone number from 0 to 9

        """
        if phone_number_length < 1:
            return -1
        elif phone_number_length == 1:
            return 10
        c = {}
        for x in range(2, phone_number_length + 1):
            nc = {}
            if x == 2:
                c = self.NUM_OF_POSSIBLE_NEXT_DIGIT
            else:
                for i in range(10):
                    nc[i] = sum((c[j] for j in self.DIGIT_MAP[i]))
                c = nc
        return sum(c.values())

    def test(self):
        results = {-1: -1,
                   0: -1,
                   1: 10,
                   2: 30,
                   3: 96,
                   4: 304,
                   5: 970,
                   6: 3094,
                   7: 9896,
                   8: 31696,
                   9: 101706,
                   10: 326862,
                   100: 8346333168977851537223946938790914315535720036672688}
        for k, v in results.items():
            print "PASS" if self.run(k) == v else "FAIL"


if __name__ == '__main__':
    m = Motif()
    m.test()
    print m.run(10)
    print m.run(100)
