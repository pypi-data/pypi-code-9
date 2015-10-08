# coding=utf8

from toolkit import ulib


def test_is_cn():
    assert ulib.is_cn(u'中')
    assert not ulib.is_cn(u'c')
    try:
        ulib.is_cn('中')
    except Exception as e:
        assert isinstance(e, ulib.NotUnicodeException)


def test_is_digital():
    assert ulib.is_digital(u'9')
    assert not ulib.is_digital(u'q')


def test_has_cn():
    assert ulib.has_cn(u'Here is a 中文 character.')
    assert not ulib.has_cn(u'Here is not any chinese character.')


def test_cn_len():
    assert ulib.cnlen(u'Here is en') == 10
    assert ulib.cnlen(u'Here is 中文') == 12


def test_c2h():
    # TODO: Coverage all full-width character
    origin = u'｀1234567890-＝～！@＃$％……&＊（）——＋［］、｛｝｜；‘：“，。／《》？'
    dest = u'`1234567890-=~!@#$%^&*()_+[]\\{}|;\':",./<>?'
    #assert ulib.f2h(origin) == dest
    pass