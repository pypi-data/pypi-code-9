# -*- coding: utf-8 -*-
""" Run is the main function that will check if the recode and bibtex
modules are working """


def check_recode():
    try:
        import recode

    except SystemError:
        raise RuntimeError('the recode library is probably broken.')

    # First, check if the recode version has the famous 3.6 bug
    rq = recode.request('UTF-8..latex')

    if recode.recode(rq, 'abc') != 'abc':
        raise RuntimeError('the _recode module is broken.')

    return 0


def expected_result(obtained, valid):
    if obtained == valid:
        return True
    try:
        return eval(obtained) == eval(valid)
    except SyntaxError:
        return False


def run():
    failures = 0
    failures += check_recode()
    raise RuntimeError

    return failures
