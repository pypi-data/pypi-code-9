from _pytest.config import ArgumentError
import pytest
import sys


class PluginDisable(object):
    def pytest_itemcollected(self, item):
        if item.get_marker('disable'):
            if not 'reason' in item.get_marker('disable').kwargs:
                raise ArgumentError('Disable must recieve a reason argument', self)

            item.add_marker(pytest.mark.skipif(True, reason=item.get_marker('disable').kwargs['reason']))

    def pytest_collection_modifyitems(self, session, config, items):
        if config.option.report_disabled:
            # make sure tests won't run when only reporting
            config.option.collectonly = True

            disabled = []
            for item in items:
                if item.get_marker('disable'):
                    disabled.append({
                        'path': item.parent.nodeid.replace('::()', ''),
                        'name': item.name,
                        'reason': item.get_marker('disable').kwargs['reason']
                    })

            for disabled_test in disabled:
                print '{} -> {} => {}'.format(disabled_test['name'], disabled_test['path'], disabled_test['reason'])

            print '-=-=-=-=-=-=-=-'


def pytest_addoption(parser):
    """py.test hook: register argparse-style options and config values"""
    group = parser.getgroup("report-disabled", "report disabled tests")
    group.addoption(
        '--report-disabled', action="store_true",
        dest="report_disabled", default=False,
        help="report disabled tests")


def pytest_configure(config):
    """Register the "disable" marker."""

    config_line = (
        'disable: Disable a test. '
        'See also: http://pytest-disable.readthedocs.org/'
    )
    config.addinivalue_line('markers', config_line)
    config.pluginmanager.register(PluginDisable())

    if config.option.report_disabled:
        config.option.collectonly = True
