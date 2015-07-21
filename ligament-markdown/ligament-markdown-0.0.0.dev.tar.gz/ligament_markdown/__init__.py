""" Basic SCSS compilation for the `ligament` task automator 
Extends the template provided by `ligament_precompiler_template`
"""
import os
import codecs
import markdown
import traceback

from ligament_precompiler_template import Precompiler
from ligament.exceptions import TaskExecutionException

class Markdown(Precompiler):
    """ An SCSS precompiler, extending the precompiler provided by
        ligament_precompiler_template
    """

    inline_template_string = "%s"
    embed_template_string = """
<html>
<body>
%s
</body>
</html>
"""

    default_kwargs = {
        "minify": False,
        "inline": False,
        "source_dir": "md",
        "target_dir": "html",
        "build_targets": ["*"],
        "relative_directory": ".",
        "md_opts": {}
    }

    def __init__(self, **kwargs):
        calling_kwargs = Markdown.default_kwargs.copy()
        calling_kwargs.update(**kwargs)

        self.md_opts = calling_kwargs["md_opts"];
        del calling_kwargs["md_opts"]

        Precompiler.__init__(self, **calling_kwargs)

        print self.file_watch_targets

    def out_path_of(self, in_path):
        relative_path = os.path.relpath(in_path, self.input_directory)
        relative_path = os.path.splitext(relative_path)[0] + ".html"
        opath = os.path.join(self.output_directory, relative_path)
        return opath

    def compile_file(self, in_path):
        try:
            with codecs.open(in_path, mode="r", encoding="utf-8") as f:
                return markdown.markdown(f.read(), **self.md_opts)
        except Exception as e:
            traceback.print_exc(e)
