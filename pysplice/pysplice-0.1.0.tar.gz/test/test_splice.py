import pytest

from pysplice import splice, mkpipe

def test_pipefiles():
    r, w = mkpipe()
    with open('/dev/zero', 'rb') as zero, open('target', 'w+b') as target:
        n1 = splice(zero, 0, w, None, 100000)
        n2 = splice(r, None, target, 0, 100000)
        assert n1 == n2
        target.seek(0)
        assert b'\0' * n2 == target.read()
