from distutils.dist import Distribution

from flexmock import flexmock


def test_version():
    # mock distutils, because of command line parsing error
    flexmock(Distribution,
        parse_command_line=lambda a: False
        )

    from cleanenv import setup

    version = setup._version()
    assert version
