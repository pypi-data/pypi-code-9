import hashlib
import os
import subprocess

from jirafs.plugin import Plugin, PluginOperationError, PluginValidationError


class GraphvizMixin(object):
    INPUT_EXTENSIONS = ['dot']
    OUTPUT_EXTENSION = 'png'

    def _get_command_args(self, input_filename, output_filename):
        command = [
            'dot',
            '-T%s' % self.OUTPUT_EXTENSION,
            input_filename,
            '-o',
            output_filename,
        ]

        return command

    def _build_output(self, input_filename, output_filename):
        proc = subprocess.Popen(
            self._get_command_args(input_filename, output_filename),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()

        if proc.returncode:
            raise PluginOperationError(
                "%s encountered an error while compiling from %s to %s: %s" % (
                    self.plugin_name,
                    input_filename,
                    output_filename,
                    stderr,
                )
            )

    def validate(self):
        try:
            subprocess.check_call(
                [
                    'dot',
                    '-V',
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except (subprocess.CalledProcessError, IOError, OSError):
            raise PluginValidationError(
                "%s requires graphviz (dot) to be installed." % (
                    self.plugin_name,
                )
            )


class Graphviz(Plugin, GraphvizMixin):
    """ Converts .dot files into PNG images using Graphviz for JIRA."""
    MIN_VERSION = '0.9.0'
    MAX_VERSION = '1.99.99'

    def get_ignore_globs(self):
        return ['*.dot']

    def run_build_process(self):
        plugin_meta = self.get_metadata()
        transformation_cache = plugin_meta.get('transformation_cache', {})

        filenames = os.listdir('.')

        transformed = []
        untransformed = []
        for input_filename in filenames:
            basename, extension = os.path.splitext(input_filename)
            if extension.lstrip('.') not in self.INPUT_EXTENSIONS:
                continue

            output_filename = '.'.join([basename, self.OUTPUT_EXTENSION])
            with open(input_filename, 'r') as inp:
                data_hash = hashlib.sha256(inp.read()).hexdigest()

            previously_transformed = (
                transformation_cache.get(input_filename) == data_hash
            )
            file_exists = os.path.exists(output_filename)

            if not (file_exists and previously_transformed):
                transformed.append(input_filename)
                self._build_output(input_filename, output_filename)

                transformation_cache[input_filename] = data_hash
            else:
                untransformed.append(input_filename)

        plugin_meta['transformation_cache'] = transformation_cache
        self.set_metadata(plugin_meta)

        lines = []
        if transformed:
            lines.append(
                'Transformed: %s' % ', '.join(transformed),
            )
        if untransformed:
            lines.append(
                'Cached: %s' % ', '.join(untransformed),
            )

        return '\n'.join(lines)
