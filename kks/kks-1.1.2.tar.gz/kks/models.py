# coding=utf8

"""
    kks.models
    ~~~~~~~~~~

    kks's models: blog, author, post, page
"""

from . import src_ext, out_ext, src_dir, out_dir
from .utils import join
from hashlib import md5


class Blog(object):
    """The blog
    attributes
      short_name    unicode     blog's short_name
      long_name     unicode     blog's long_name
      theme         str         blog's theme"""

    def __init__(self, short_name="", long_name="", theme=""):
        self.short_name = short_name
        self.long_name  = long_name
        self.theme = theme


blog = Blog()


class Author(object):
    """The blog's owner, only one
    attributes
      name      unicode     author's name
    """

    def __init__(self, name=""):
        self.name = name

author = Author()


class Post(object):
    """The blog's post object.
    attributes
      name      unicode     post's filename without extension
      title     unicode     post's title
      time      unicode     post's created time
      tag       unicode     post's tag
      markdown  unicode     post's body source, it's in markdown
      html      unicode     post's html, parsed from markdown
      summary   unicode     post's summary
      filepath  unicode     post's filepath
    """

    src_dir = src_dir
    out_dir = join(out_dir, "post")
    template = "post.html"

    def __init__(self, name="", title="", time="", tag="", markdown="",
                 html="", summary="", filepath="",):
        self.name = name
        self.title = title
        self.time = time
        self.tag = tag
        self.markdown = markdown
        self.html = html
        self.summary = summary
        self.filepath = filepath

    @property
    def src(self):
        return join(Post.src_dir, self.name + src_ext)

    @property
    def out(self):
        return join(Post.out_dir, self.name + out_ext)


class Page(object):
    """The 1st, 2nd, 3rd page..
    attributes
      number    int         the page's order
      posts     list        lists of post objects
      first     bool        is the first page?
      last      bool        is the last page?"""

    template = "page.html"
    out_dir = join(out_dir, "page")

    def __init__(self, number=1, posts=None, first=False, last=False):
        self.number = number
        self.first = first
        self.last = last

        if posts is None:
            self.posts = []
        else:
            self.posts = posts

    @property
    def out(self):
        if self.first:
            return join(out_dir, "index" + out_ext)
        else:
            return join(Page.out_dir, str(self.number) + out_ext)
