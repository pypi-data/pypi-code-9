# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)

from pynleq2 import solve


def test_solve():
    def f(x, i):
        return [x[0] + (x[0] - x[1])**3/2 - 1,
                (x[1] - x[0])**3/2 + x[1]], i

    def j(x):
        return [
            [
                1 + 3/2 * (x[0] - x[1])**(3-1),
                -3/2 * (x[0] - x[1])**(3-1)
            ],
            [
                -3/2 * (x[1] - x[0])**(3-1),
                1 + 3/2 * (x[1] - x[0])**(3 - 1)
            ]
        ]

    x, ierr = solve(f, j, [0, 1])
    assert abs(x[0] - 0.8411639) < 2e-7
    assert abs(x[1] - 0.1588361) < 2e-7
