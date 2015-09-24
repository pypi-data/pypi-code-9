import os
import sys
import time

from okapi.core.exceptions import OkapiException
from okapi.core.utils import publish
from okapi.rst.directives import load_directives
from okapi.settings import settings


class NotRendered(OkapiException):
    pass


class Runner(object):
    template_name = 'base.html'

    def __init__(self, file=None, url=None):
        """
        Initializes runner instance.

        :param file: RST file with documentation.
        :type file: str

        :param url: URL against which requests are made.
        :type url: str
        """
        load_directives()
        self.file = settings.file = file or settings.file
        self.url = settings.url = url or settings.url
        self.rendered = None

    def run(self):
        settings.internal.summary.time_start = time.time()
        self.render()

        if settings.output:
            self.save(settings.output)

        settings.internal.summary.time_end = time.time()
        self.print_summary()
        sys.exit(0 if settings.internal.status else 1)

    def render(self):
        """
        Renders file and returns rendered HTML.

        :return: Rendered HTML string.
        :rtype: str
        """
        template = settings.template.env.get_template(self.template_name)
        self.rendered = template.render(**self.get_context_data())

        return self.rendered

    def save(self, output):
        """
        Saves rendered HTML to file.

        :param output: Path to output file
        :type output: str

        :raise NotRendered: In case of empty self.rendered string.
        """
        if not self.rendered:
            raise NotRendered

        if not os.path.isdir(output):
            os.mkdir(output)

        index = os.path.join(output, 'index.html')
        open(index, 'w', encoding='utf8').write(self.rendered)
        os.system('cp -r {}/static {}/'.format(settings.internal.path, output))

    def get_context_data(self):
        """
        Parses input RST file and prepare dictionary for passing to template.

        :return: Dictionary passed to template.
        :rtype: dict
        """
        parts = publish(open(self.file).read(), path=settings.source_path)
        return dict(
            title=parts['html_title'],
            content=parts['html_body'],
            settings=settings
        )

    @staticmethod
    def print_summary():
        log = settings.log
        summary = settings.internal.summary

        if settings.log.verbosity == 0:
            return

        log.error('')
        log.write('Tests count: {}'.format(summary.count))
        log.write('Failed tests count: {}'.format(summary.failed))
        log.write('Time elapsed: {0:.2f} s'.format(summary.time_elapsed))

        if summary.failed_tests:
            log.write('\nFailed tests:')
            for test in summary.failed_tests:
                log.write('- {}: {} {}'.format(*test))
