__author__ = 'ilysenko'

import nose
from nose.plugins.plugintest import run_buffered as run
from nose_html_reporting import HtmlReport


args = ['-v',
        'test_sample.py',
        '--with-html',
        '--html-report=../nose_report2_test.html']
        # '--html-report-template=../src/nose_html_reporting/templates/report2.jinja2']
nose.run(argv=args, plugins=[HtmlReport()])