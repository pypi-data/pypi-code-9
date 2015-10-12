import hashlib
import os
import subprocess

import six

from jirafs.plugin import (
    BlockElementMacroPlugin, Plugin,
    PluginOperationError, PluginValidationError
)


class LatexMixin(object):
    def _get_command_args(self, filename):
        command = [
            'xelatex',
            '-shell-escape',
            filename
        ]

        return command

    def _build_output(self, input_filename, output_filename, preserve=None):
        existing_files = os.listdir('.')

        basename, extension = os.path.splitext(input_filename)
        proc = subprocess.Popen(
            self._get_command_args(input_filename),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()

        if preserve is None:
            preserve = []

        if proc.returncode:
            raise PluginOperationError(
                "%s encountered an error while compiling PDF for %s: %s" % (
                    self.plugin_name,
                    input_filename,
                    stderr,
                )
            )

        with open(output_filename, 'rb') as temp_output:
            content = six.BytesIO(temp_output.read())

        final_files = os.listdir('.')
        to_delete = set(final_files) - set(preserve) - set(existing_files)

        for filename in to_delete:
            os.unlink(filename)

        return content

    def validate(self):
        try:
            subprocess.check_call(
                ['xelatex', '--version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except (subprocess.CalledProcessError, IOError, OSError):
            raise PluginValidationError(
                "%s requires xelatex to be installed." % (
                    self.plugin_name,
                )
            )


class Latex(Plugin, LatexMixin):
    """ Converts Latex documents into PDFs when uploading to JIRA.

    """
    MIN_VERSION = '1.16'
    MAX_VERSION = '1.99.99'

    LATEX_EXTENSIONS = ['tex']

    def get_ignore_globs(self):
        return ['*.tex']

    def run_build_process(self):
        plugin_meta = self.get_metadata()
        transformation_cache = plugin_meta.get('transformation_cache', {})

        filenames = os.listdir('.')

        transformed = []
        untransformed = []
        for input_filename in filenames:
            basename, extension = os.path.splitext(input_filename)
            if extension.lstrip('.') not in self.LATEX_EXTENSIONS:
                continue

            output_filename = '.'.join([basename, 'pdf'])

            with open(input_filename, 'r') as inp:
                data_hash = hashlib.sha256(inp.read()).hexdigest()

            previously_transformed = (
                transformation_cache.get(input_filename) == data_hash
            )
            file_exists = os.path.exists(output_filename)

            if not (file_exists and previously_transformed):
                transformed.append(input_filename)
                self._build_output(
                    input_filename,
                    output_filename,
                    preserve=[output_filename],
                )

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


class LatexBlock(BlockElementMacroPlugin, LatexMixin):
    MIN_VERSION = '1.16'
    MAX_VERSION = '2.0.0'
    COMPONENT_NAME = 'latex'

    def execute_macro(self, data, **parameters):
        plugin_meta = self.get_metadata()
        transformation_cache = plugin_meta.get('transformation_cache', {})

        if 'name' not in parameters:
            raise PluginOperationError(
                "You must specify a 'name' parameter for each 'latex' block'"
            )

        output_filename = parameters['name']
        basename, extension = os.path.splitext(output_filename)
        input_filename = '.'.join([basename, 'tex'])

        data_hash = hashlib.sha256(data).hexdigest()

        previously_transformed = (
            transformation_cache.get(input_filename) == data_hash
        )
        file_exists = os.path.exists(output_filename)
        if not (file_exists and previously_transformed):
            with open(input_filename, 'w') as out:
                out.write(data)

            self._build_output(
                input_filename,
                output_filename,
                preserve=[output_filename],
            )

            os.unlink(input_filename)
            transformation_cache[input_filename] = data_hash

        plugin_meta['transformation_cache'] = transformation_cache
        self.set_metadata(plugin_meta)

        return u"!{filename}!".format(filename=output_filename)
