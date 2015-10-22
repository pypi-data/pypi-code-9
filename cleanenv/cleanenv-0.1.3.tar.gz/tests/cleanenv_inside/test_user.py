import grp
import os
import pwd
import pytest
from flexmock import flexmock
from cleanenv.cleanenv_inside.user import expand_user, username_from_config


def test_expand_user_invalid():
    with pytest.raises(ValueError):
        expand_user({'global': {'user': 'abc:tester'}})


@pytest.mark.parametrize('value, expect', [
    ('system:', None),
    (None, None),
    ('', None),
    (':1:', None),
    ('tester', 'tester'),
    ('te-st_er7', 'te-st_er7'),
    ('net+tester', 'net+tester'),
])
def test_username_from_config(value, expect):
    result = username_from_config({'global': {'user': value}})
    assert result == expect


groups = [
    {'name': 'gx', 'gid': 100},
    {'name': 'g2', 'gid': 102},
    {'name': '.g-___3', 'gid': 103, 'comment': '.g-$ +3'},
    {'name': 'veryveryveryveryveryverylongname',
        'gid': 104, 'comment': 'veryveryveryveryveryverylongname_thisnot'}]

@pytest.mark.parametrize('value, expect', [
    ('4444:',
     dict(name='tester', uid=4444, system=False, sudo=False, groups=groups)),

    ('',
     dict(name='tester', uid=1234, system=False, sudo=False, groups=groups)),

    ('system:',
     dict(name='tester', uid=1234, system=True, sudo=False, groups=groups)),

    ('system::daemon',
     dict(name='daemon', uid=1234, system=True, sudo=False,
          groups=[{'name': 'gx', 'gid': 100}])),
])
def test_expand_user(value, expect):
    struct = pwd.struct_passwd(
        ['tester', 'x', 1234, 1000, 'Test User', '/home/tester', '/bin/sh'])
    flexmock(os) \
        .should_receive('geteuid') \
        .and_return(1234)
    flexmock(pwd) \
        .should_receive('getpwuid') \
        .and_return(struct)
    flexmock(pwd) \
        .should_receive('getpwnam') \
        .and_return(struct)
    flexmock(grp) \
        .should_receive('getgrnam') \
        .and_return(grp.struct_group(['gx', 'x', 100, []]))
    flexmock(grp) \
        .should_receive('getgrall') \
        .and_return([
            grp.struct_group(['g1', 'x', 101, []]),
            grp.struct_group(['g2', 'x', 102, ['tester']]),
            grp.struct_group(['.g-$ +3', 'x', 103, ['net+tester']]),
            grp.struct_group(['veryveryveryveryveryverylongname_thisnot',
                'x', 104, ['tester']]),
        ])

    result = expand_user({'global': {'user': value}})
    assert result == expect


def test_expand_user_non_posix():
    longname  = 'This+is-not@a-posix-username.It-is-also-very-long'
    shortname = longname[:32]
    posixname = 'This_is-not_a-posix-username.It-'

    struct = pwd.struct_passwd(
        [longname, 'x', 1234, 1000, 'Test User', '/home/tester', '/bin/sh'])
    flexmock(pwd) \
        .should_receive('getpwnam') \
        .and_return(struct)
    flexmock(grp) \
        .should_receive('getgrnam') \
        .and_return(grp.struct_group(['gx', 'x', 100, []]))
    flexmock(grp) \
        .should_receive('getgrall') \
        .and_return([
            grp.struct_group(['g1', 'x', 101, [longname]]),
            grp.struct_group(['g2', 'x', 102, [shortname]]),
            grp.struct_group(['g3', 'x', 103, [posixname]]),
        ])

    result = expand_user({'global': {'user': '1234:' + longname}})
    expect = dict(
        name=posixname,
        uid=1234,
        system=False,
        sudo=False,
        comment=longname,
        groups=[{'name': 'gx', 'gid': 100},
                {'name': 'g1', 'gid': 101}])
    assert result == expect


def test_expand_user_no_such_user():
    # user does not exist on the system
    flexmock(pwd).should_receive('getpwnam').and_raise(KeyError)

    result = expand_user({'global': {'user': 'tester'}})

    expect = dict(name='tester', uid=None, system=False, groups=[], sudo=False)
    assert result == expect
