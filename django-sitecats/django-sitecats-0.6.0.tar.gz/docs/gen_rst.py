import sphinx.ext.autodoc
rst = []
def add_line(self, line, source, *lineno):
    """Append one line of generated reST to the output."""
    rst.append(line)
    self.directive.result.append(self.indent + line, source, *lineno)
sphinx.ext.autodoc.Documenter.add_line = add_line
try:
    sphinx.main(['sphinx-build', '-b', 'html', '-d', '_build/doctrees', 'source/', '_build/html'])
except SystemExit:
    with file('docaaaa.rst', 'w') as f:
        for line in rst:
            print >>f, line
