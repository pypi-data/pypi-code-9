# encoding: UTF-8
# Copyright (C) 2007-2010, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
HTML templates for use in Websourcebrowser.
"""

TOP = u"""\
<h1><span id="top_path">%(path)s</span></h1>
"""

#XXX maybe remove the padding with JavaScript in the Ajax version:
#  move contents to the same level as the div is now at
DIRECTORY = u"""\
<div>
    <a href="#" id="level_1">1</a>&nbsp;&nbsp;
    <a href="#" id="level_minus">&ndash;</a>
    <input type="text" id="current_level" size="2" maxlength="2" value="1" />
    <a href="#" id="level_plus">+</a>&nbsp;&nbsp;
    <a href="#" id="level_all">all</a><br />
    %(content)s
</div>
"""

#XXX maybe remove the padding with JavaScript in the Ajax version:
#  move contents to the same level as the div is now at
FILE = u"""\
<div>
    %(content)s
</div>
"""

PAGE = u"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <link rel="stylesheet" type="text/css"
          href="/%(static_dir)s/jquery.treeview.css" />
    <link rel="stylesheet" type="text/css"
          href="/%(static_dir)s/websourcebrowser.css" />
    <title>%(title)s - %(project_title)s</title>
    <script src="/%(static_dir)s/jquery-1.4.2.js"></script>
    <script src="/%(static_dir)s/jquery-ui-1.8.js"></script>
    <script src="/%(static_dir)s/jquery.layout-1.3.0.rc28.js"></script>
    <script src="/%(static_dir)s/jquery.treeview.js"></script>
    <script src="/%(static_dir)s/websourcebrowser.js"></script>
</head>
<body>
    <div id="top" class="top top_preset">
        %(top)s
    </div>
    <div id="dir" class="dir_preset">
        %(dir_)s
    </div>
    <div id="file" class="file_preset">
        %(file_)s
    </div>
</body>
</html>
"""

