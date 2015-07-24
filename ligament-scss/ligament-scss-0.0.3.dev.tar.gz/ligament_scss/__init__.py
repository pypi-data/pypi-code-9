""" Basic SCSS compilation for the `ligament` task automator 
Extends the template provided by `ligament_precompiler_template`
"""
import os
import scss

from ligament_precompiler_template import Precompiler
from ligament.helpers import mkdir_recursive, map_over_glob, zip_with_output
from ligament.exceptions import TaskExecutionException

class Scss(Precompiler):
    """ An SCSS precompiler, extending the precompiler provided by
        ligament_precompiler_template
    """

    external_template_string = (
        "<link rel='stylesheet' type='text/css' href='%s'></link>")

    embed_template_string = "<style>%s</style>"

    default_kwargs = {
        "minify": True,
        "embed": True,
        "source_dir": "template/css",
        "target_dir": "build/css",
        "build_targets": ["*"],
        "relative_directory": "./css/"
    }

    def __init__(self, **kwargs):
        calling_kwargs = Scss.default_kwargs.copy()
        calling_kwargs.update(**kwargs)
        Precompiler.__init__(self, **calling_kwargs)

        self.compiler = scss.Scss({"compress": self.minify})
        self.compiler_name = "scss"

        self.file_watch_targets = [
            os.path.join(self.input_directory, "*.scss"),
            os.path.join(self.input_directory, "*.css")]

    def out_path_of(self, in_path):
        relative_path = os.path.relpath(in_path, self.input_directory)

        if relative_path.endswith(".scss"):
            relative_path = relative_path[0:-4]+"css"

        return os.path.join(self.output_directory, relative_path)

    def compile_file(self, in_path):
        try:
            compiled_string = self.compiler.compile(scss_file=in_path)
        except scss.errors.SassBaseError as e:
            raise TaskExecutionException(
                "Error compiling style %s:" % in_path,
                (e.format_sass_stack() +
                 e.expression +
                 e.expression_pos * " " + "^").replace(
                    "\n", "\n     "))

        return compiled_string
