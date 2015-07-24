
from chores import *
import time
import pytest

def almost_equals(a, b, delta=0.01):
    """
    Is a almost equal to b?
    """
    return abs(a - b) < delta

@pytest.mark.skipif(True, reason="functionality not ready")
def test_stages():
    st = Stages('a b c'.split())
    time.sleep(0.4)
    st.begin('a')
    time.sleep(1.5)
    st.begin('b')
    time.sleep(1.8)
    st.end('a')
    st.end('b')
    with st.enter('c'):
        time.sleep(2.0)
    d = st.durations()

    assert almost_equals(d.overall, 5.7)
    assert almost_equals(d.a, 3.3)
    assert almost_equals(d.b, 1.8)
    assert almost_equals(d.c, 2.0)
