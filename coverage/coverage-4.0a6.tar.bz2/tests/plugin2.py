"""A plugin for test_plugins.py to import."""

import os.path

import coverage

# pylint: disable=missing-docstring


class Plugin(coverage.CoveragePlugin):
    def file_tracer(self, filename):
        if "render.py" in filename:
            return RenderFileTracer()

    def file_reporter(self, filename):
        return FileReporter(filename)


class RenderFileTracer(coverage.plugin.FileTracer):
    """A FileTracer using information from the caller."""

    def has_dynamic_source_filename(self):
        return True

    def dynamic_source_filename(self, filename, frame):
        if frame.f_code.co_name != "render":
            return None
        source_filename = os.path.abspath(frame.f_locals['filename'])
        return source_filename

    def line_number_range(self, frame):
        lineno = frame.f_locals['linenum']
        return lineno, lineno+1


class FileReporter(coverage.plugin.FileReporter):
    def statements(self):
        # Goofy test arrangement: claim that the file has as many lines as the
        # number in its name.
        num = os.path.basename(self.filename).split(".")[0].split("_")[1]
        return set(range(1, int(num)+1))
