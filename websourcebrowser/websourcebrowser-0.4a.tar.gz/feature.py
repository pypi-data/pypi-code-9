# encoding: UTF-8
# Copyright (C) 2010, Stefan Schwarzer

"""
Determine if the system Websourcebrowser runs on has certain features.

For example, `feature.pygments` tells whether the system has the
Pygments syntax highlighting package installed and in the module
search path.
"""

# Pygments - syntax highlighting
try:
    import pygments as pygments_package
    from pygments import lexers
    del lexers
    from pygments import formatters
    del formatters
    pygments = True
except ImportError:
    pygments = False


# Cherrypy - robust multi-threaded server
try:
    import cherrypy as cherrypy_package
except ImportError:
    cherrypy = False
else:
    # Websourcebrowser server is programmed with CherryPy 3.x's API in mind
    cherrypy = cherrypy_package.__version__.startswith("3.")


# Exuberant ctags - class/method/function tree

