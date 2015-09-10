import os
import pytest
from _pytest.config import ArgumentError


class PluginDisable(object):
    def pytest_itemcollected(self, item):
        if item.get_marker('disable'):
            if 'reason' not in item.get_marker('disable').kwargs:
                raise ArgumentError('Disable must recieve a reason argument', self)

            item.add_marker(pytest.mark.skipif(True, reason=item.get_marker('disable').kwargs.get('reason')))

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
                        'reason': item.get_marker('disable').kwargs.get('reason')
                    })

            f = open(config.option.disabled_report_file, 'w')
            for disabled_test in disabled:
                line = '{} -> {} => {}'.format(disabled_test['name'], disabled_test['path'], disabled_test['reason'])
                print line
                f.write(line + '\n')

            summary = '============================ Found {} disabled tests ============================'.format(
                len(disabled))
            print summary
            f.write('\n'+summary)
            f.close()


def pytest_addoption(parser):
    """py.test hook: register argparse-style options and config values"""
    group = parser.getgroup("report-disabled", "report disabled tests")
    group.addoption(
        '--report-disabled', action="store_true",
        dest="report_disabled", default=False,
        help="report disabled tests")
    group.addoption(
        '--disabled-report-file', dest="disabled_report_file",
        default='/tmp/disabled_report.txt',
        help="disabled tests report file")


def pytest_configure(config):
    """Register the "disable" marker."""

    config_line = (
        'disable: Disable a test. '
        'See also: http://pytest-disable.readthedocs.org/'
    )
    config.addinivalue_line('markers', config_line)
    config.pluginmanager.register(PluginDisable())

    if config.option.report_disabled:
        # Set pytest to only collect tests and not run them
        config.option.collectonly = True

        report_file_dir = os.path.dirname(config.option.disabled_report_file)
        if not os.path.isdir(report_file_dir):
            os.makedirs(report_file_dir)
