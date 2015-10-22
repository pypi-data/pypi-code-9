import os
from cleanenv.cleanenv_inside.flock import UsageCounter


def test_usage_counter_do_nothing(tmpdir):
    path     = tmpdir.join('counter').strpath
    lockpath = path + '.lock'

    with UsageCounter(path) as f:
        assert os.path.exists(lockpath)
        assert not os.path.exists(path)

    assert not os.path.exists(lockpath)
    assert not os.path.exists(path)


def test_usage_counter(tmpdir):
    path     = tmpdir.join('counter').strpath
    lockpath = path + '.lock'

    # 4 x incr
    for i in [1, 2, 3, 4]:
        with UsageCounter(path) as f:
            value = f.incr()
            assert value == i

            assert os.path.exists(lockpath)
            assert os.path.exists(path)

        assert not os.path.exists(lockpath)
        assert os.path.exists(path)
        assert open(path).read() == '%d' % i

    # 4 x decr
    for i in [3, 2, 1, 0]:
        with UsageCounter(path) as f:
            value = f.decr()
            assert value == i

        assert open(path).read() == '%d' % i

    # more decr, still 0
    with UsageCounter(path) as f:
        value = f.decr()
        assert value == 0

    assert open(path).read() == '0'


def test_usage_counter_bad_file_content(tmpdir):
    path = tmpdir.join('counter').strpath

    open(path, 'w').write('not-a-number')

    with UsageCounter(path) as f:
        value = f.incr()
        assert value == 1
