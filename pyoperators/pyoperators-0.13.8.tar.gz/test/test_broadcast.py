from numpy.testing import assert_equal
from pyoperators import Operator, operation_assignment
from pyoperators.core import _pool
from pyoperators.utils.testing import assert_same
from pyoperators.flags import handle_broadcast
import numpy as np


data = np.array([[0, 1], [1, 2], [2, 3]])
m = data.shape[0]
n = data.shape[1]


class MyOperator(Operator):
    def direct(self, input, output):
        np.dot(data, input, out=output)


class ExplExpl(MyOperator):
    def __init__(self, **keywords):
        MyOperator.__init__(self, shapein=n, shapeout=m, **keywords)


@handle_broadcast('leftward')
class ExplExplLeft(ExplExpl):
    pass


@handle_broadcast('rightward')
class ExplExplRight(ExplExpl):
    def direct(self, input, output):
        np.dot(data, input.T, out=output.T)


class ExplUnco(MyOperator):
    def __init__(self, **keywords):
        MyOperator.__init__(self, shapeout=m, naxesin=1, **keywords)


@handle_broadcast('leftward')
class ExplUncoLeft(ExplUnco):
    pass


@handle_broadcast('rightward')
class ExplUncoRight(ExplUnco):
    def direct(self, input, output):
        np.dot(data, input.T, out=output.T)


class UncoExpl(MyOperator):
    def __init__(self, **keywords):
        MyOperator.__init__(self, shapein=n, naxesout=1, **keywords)


@handle_broadcast('leftward')
class UncoExplLeft(UncoExpl):
    pass


@handle_broadcast('rightward')
class UncoExplRight(UncoExpl):
    def direct(self, input, output):
        np.dot(data, input.T, out=output.T)


class ImplImpl(MyOperator):
    def __init__(self, **keywords):
        MyOperator.__init__(self, naxesin=1, naxesout=1, **keywords)

    def reshapein(self, shape):
        return (m,)

    def reshapeout(self, shape):
        return (n,)


@handle_broadcast('leftward')
class ImplImplLeft(ImplImpl):
    pass


@handle_broadcast('rightward')
class ImplImplRight(ImplImpl):
    def direct(self, input, output):
        np.dot(data, input.T, out=output.T)


class ImplUnco(MyOperator):
    def __init__(self, **keywords):
        MyOperator.__init__(self, naxesin=1, naxesout=1, **keywords)

    def reshapein(self, shape):
        return (m,)


@handle_broadcast('leftward')
class ImplUncoLeft(ImplUnco):
    pass


@handle_broadcast('rightward')
class ImplUncoRight(ImplUnco):
    def direct(self, input, output):
        np.dot(data, input.T, out=output.T)


class UncoImpl(MyOperator):
    def __init__(self, **keywords):
        MyOperator.__init__(self, naxesin=1, naxesout=1, **keywords)

    def reshapeout(self, shape):
        return (n,)


@handle_broadcast('leftward')
class UncoImplLeft(UncoImpl):
    pass


@handle_broadcast('rightward')
class UncoImplRight(UncoImpl):
    def direct(self, input, output):
        np.dot(data, input.T, out=output.T)


def repeat_iter(iterable, n=1):
    for _ in iterable:
        for i in xrange(n):
            yield _


cls = (ExplExpl, ExplExplLeft, ExplExplRight,
       ExplUnco, ExplUncoLeft, ExplUncoRight,
       UncoExpl, UncoExplLeft, UncoExplRight,
       ImplImpl, ImplImplLeft, ImplImplRight,
       ImplUnco, ImplUncoLeft, ImplUncoRight,
       UncoImpl, UncoImplLeft, UncoImplRight)


def test_nobroadcast():
    def func(cls, k, b):
        op = cls(broadcast=b)
        assert_equal(cls.__name__[:8].lower(),
                     op.flags.shape_output[:4] + op.flags.shape_input[:4])
        assert_same(op.todense(**k), data)
    keywords = repeat_iter(({},
                            {'shapein': n},
                            {'shapeout': m},
                            {'shapein': n},
                            {'shapein': n},
                            {'shapeout': m}), n=3)
    for cls_, keywords_ in zip(cls, keywords):
        for b in 'leftward', 'rightward':
            yield func, cls_, keywords_, b


def test_broadcast():
    def p(s, k):
        if broadcast == 'leftward':
            return s + (k,)
        return (k,) + s

    def func(bshape, broadcast, cls, keywords):
        op = cls(broadcast=broadcast)
        if broadcast == 'leftward':
            dense = np.kron(np.eye(np.product(bshape)), data)
        else:
            dense = np.kron(data, np.eye(np.product(bshape)))
        assert_same(op.todense(**keywords), dense)
    for bshape in (1,), (2,), (2, 1), (1, 2), (2, 3):
        for broadcast in 'leftward', 'rightward':
            keywords = repeat_iter(({'shapein': p(bshape, n)},
                                    {'shapein': p(bshape, n)},
                                    {'shapeout': p(bshape, m)},
                                    {'shapein': p(bshape, n)},
                                    {'shapein': p(bshape, n)},
                                    {'shapeout': p(bshape, m)}), n=3)
            for cls_, keywords_ in zip(cls, keywords):
                yield func, bshape, broadcast, cls_, keywords_
