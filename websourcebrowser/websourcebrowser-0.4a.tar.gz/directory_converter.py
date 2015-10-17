# encoding: UTF-8
# Copyright (C) 2009-2010, Stefan Schwarzer

"""
Code to render a directory path to suitable HTML for the left pane.
"""

import cgi
import os

import coding
import config
import dirtree
import tools
import urlpath


def directory_listing(doc):
    """Return the `Document` `doc` with a `html` attribute containing
    HTML code for a list of directories and files, similar to the
    output of `ls -1 path` under Posix.
    """
    path = doc.path
    dt = dirtree.DirectoryTree(path)
    dt.read(depth=1)
    html_parts = []
    # directory list
    for item_type, path in dt.items:
        # icon
        if item_type == "directory":
            image_file = "folder-closed.gif"
        else:
            image_file = "file.gif"
        image_html = u'<img src="/static/%s" />' % image_file
        # name, formatted as link
        url = coding.encode_uri(u"/%s" % config.PROJECT_DIR +
                                urlpath.to_url(path, config.root))
        text = cgi.escape(os.path.basename(path))
        link = u'<a href="%s">%s</a>' % (url, text)
        # combine icon and link
        html_parts.append("%s%s" % (image_html, link))
    doc.html = u"<br />\n".join(html_parts)
    doc.mime_type = "text/html"
    return doc


class TreeviewHTML(object):
    """Scan the contents of a directory and put its HTML presentation
    into the document's `html` attribute.
    """

    def path_pairs(self, path):
        """Convert the `path` argument, a string denoting a
        directory path, to a list of (item_type, path) pairs.
        The paths are unicode strings.
        """
        # the Python documentation says `abspath` implies `normpath`
        #  "on _most_ platforms" - don't take a risk
        tree = dirtree.DirectoryTree(path)
        try:
            tree.read()
        except dirtree.ReadError:
            # consider `dirtree`'s `ReadError` an implementation detail;
            #  raise `IOError` from _this_ module
            raise IOError(u"can't scan directory '%s'" % path)
        # strip root direcory at the beginning of item strings
        if config.root == os.sep:
            to_remove = u""
        else:
            assert not config.root.endswith(os.sep)
            # `config.root` must not end with a separator
            to_remove = config.root + os.sep
        return [(priority, item[len(to_remove):])
                for (priority, item) in tree.items]

    def _dir_level(self, item):
        """Return the nesting level for the path in `item` as
        an integer.
        """
        return item.count(os.sep) - 1

    def _link_and_text(self, item):
        """Return HTML representation for a single link."""
        item = coding.encode(item)
        link = coding.encode_uri(item)
        link = coding.decode(link)
        #FIXME workaround for non-ascii characters in directory and
        #  file names; needs proper design
        text = cgi.escape(coding.decode(os.path.basename(item)))
        return u'<a href="%s">%s</a>' % (link, text)

    def to_html_list(self, path_pairs):
        """Return directory as a (possibly nested) list."""
        html_parts = [u'''<ul id="directory_tree" class="filetree"
                          style="margin-left: 0px;"><li>''']
        # if we do _not_ have `path_pairs`, the loop below doesn't use
        #  `previous_dir_level`, so it's safe to not set it in this case
        if path_pairs:
            previous_dir_level = self._dir_level(path_pairs[0][1])
        is_first_iteration = True
        for item_type, path in path_pairs:
            dir_level = self._dir_level(path)
            indentation_difference = dir_level - previous_dir_level
            if indentation_difference == 0 and not is_first_iteration:
                # finish one list item and start a new one on the same level
                html_parts.append(u"</li><li>")
            if indentation_difference > 0:
                for i in range(indentation_difference):
                    # start a new list
                    html_parts.append(u"<ul><li>")
            if indentation_difference < 0:
                for i in range(-indentation_difference):
                    # end previous list
                    html_parts.append(u"</li></ul>")
                html_parts.append(u'<li>')
            relative_url = path.replace(os.sep, urlpath.SEP)
            link = self._link_and_text("/%s/%s" %
                                       (config.PROJECT_DIR, relative_url))
            span_class = {"directory": "folder", "file": "file"}[item_type]
            escaped_title = cgi.escape(relative_url, quote=True)
            spanned_link = u'<span class="%s" title="%s">%s</span>' % \
                           (span_class, escaped_title, link)
            html_parts.append(spanned_link)
            # save reference for next iteration
            previous_dir_level = dir_level
            # this _was_ the first iteration
            is_first_iteration = False
        html_parts.append(u"</li></ul>")
        return u"\n".join(html_parts)

    def __call__(self, doc):
        """Return the document object `doc` with an `html` attribute
        for the HTML treeview representation of the path added.
        """
        path_pairs = self.path_pairs(doc.path)
        doc.html = self.to_html_list(path_pairs)
        doc.mime_type = u"text/html"
        return doc


treeview_html = TreeviewHTML()

