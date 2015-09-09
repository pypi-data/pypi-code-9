#!/usr/bin/env python2
import os
import sys
import json
import errno
import shutil
import datetime
import webbrowser
import SocketServer
import SimpleHTTPServer

from core import Processor


def usage():
    print """\
Usage: buildup [init | build]

init: initialize current directory
build: generate static blog\n"""


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def datestamp():
    today = datetime.datetime.today()
    year = str(today.year)[2:4]
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    return "".join([year, month, day])


def buildup_init():
    ds = datestamp()

    # create post and pages directory
    mkdir_p("_posts")
    mkdir_p("_pages")

    # create first post
    post_demo = open(os.path.join("_posts", ds + "-First_Post.md"), "w")
    post_demo.write("# First Post\nHello World!")
    post_demo.close()

    # create first page
    page_demo = open(os.path.join("_pages", "example_page.md"), "w")
    page_demo.write("# First Page\nHello World!")
    page_demo.close()

    # copy templates
    script_path = os.path.dirname(os.path.realpath(__file__))
    package_path = os.path.split(script_path)[0]
    templates_dir = os.path.join(package_path, "templates")
    shutil.copytree(templates_dir, os.path.join(os.getcwd(), "templates"))

    # create initial config file
    config = open("config.json", "w")
    config.write("""
{
    "pages": [
        {
            "title": "First Page",
            "file_path": "_pages/example_page.md",
            "output_dir": "html/pages",
            "template": "page.html"
        }
    ],

    "input_dir": "_posts",
    "output_dir": "html/posts",

    "templates_dir": "templates",
    "index_template": "index.html",
    "post_template": "post.html"
}
    """.strip())
    config.close()


def buildup_build():
    config = json.load(open("config.json", "r"))
    p = Processor(**config)
    p.run()


def main(args=None):
    # pre-check
    if len(sys.argv) == 1:
        usage()
        sys.exit(-1)

    # execute
    action = sys.argv[1]
    if action == "init":
        buildup_init()

    elif action == "build":
        buildup_build()

    elif action == "preview":
        print ">>>>> Press Ctrl+C to stop server <<<<<"
        webbrowser.open_new("http://127.0.0.1:8000")
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer(("", 8000), Handler)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
