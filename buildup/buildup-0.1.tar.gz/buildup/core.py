#!/usr/bin/env python
import os
import shutil
import fnmatch

import markdown
from jinja2 import Environment
from jinja2 import FileSystemLoader
from bs4 import BeautifulSoup


class Post(object):
    def __init__(self, input_dir, output_dir, post_path):
        self.file_path = post_path
        self.file_name = os.path.basename(post_path)
        self.output_path = os.path.normpath(
            os.path.join(
                output_dir,
                os.path.relpath(os.path.dirname(post_path), input_dir),
                self.file_name.replace(".md", ".html")
            )
        )
        self.href = os.path.basename(post_path)
        self.title = self.parse_title(self.file_name)
        self.created = self.parse_date(self.file_name[0:6])

    def parse_date(self, date_string):
        year = "20" + date_string[0:2]
        month = [
            "Jan", "Feb", "Mar", "Apr", "May",
            "Jun", "Jul", "Aug", "Sep", "Oct",
            "Nov", "Dec"
        ][int(date_string[2:4]) - 1]
        day = date_string[4:6]

        return "{day} {month} {year}".format(day=day, month=month, year=year)

    def parse_title(self, file_name):
        if file_name[6] != "-":
            raise RuntimeError("Invalid file name format!")

        return file_name[7:-3].replace("_", " ")


class Processor(object):
    def __init__(self, **kwargs):
        self.input_dir = kwargs.get("input_dir")
        self.post_ext = kwargs.get("post_ext", ".md")
        self.output_dir = kwargs.get("output_dir")
        self.template_dir = kwargs.get("template_dir", "templates")
        self.index_template = kwargs.get("index_template")
        self.post_template = kwargs.get("post_template")
        self.pages = self.preprocess_pages(kwargs.get("pages"))
        self.posts = self.preprocess_posts()
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def convert_md(self, file_path):
        file_contents = open(file_path, "r").read()
        return markdown.markdown(file_contents)

    def copy_dir(self):
        shutil.copytree(self.input_dir, self.output_dir)

        # remove .md files
        for root, dirnames, filenames in os.walk(self.output_dir):
            for filename in fnmatch.filter(filenames, '*' + self.post_ext):
                os.remove(os.path.join(root, filename))

    def get_posts(self):
        matches = []
        for root, dirnames, filenames in os.walk(self.input_dir):
            for filename in fnmatch.filter(filenames, '*' + self.post_ext):
                matches.append(os.path.join(root, filename))

        return matches

    def preprocess_posts(self):
        post_files = self.get_posts()
        posts = []

        # pre-check
        if post_files is None or len(post_files) == 0:
            err_msg = "found no posts @ [{0}] with file ext [{1}]".format(
                self.input_dir,
                self.post_ext
            )
            raise RuntimeError(err_msg)

        # create post objects
        for post_file in post_files:
            posts.append(Post(self.input_dir, self.output_dir, post_file))

        return posts

    def purge_dirs(self):
        # purge posts output dir
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

        # purge pages output dir
        for page in self.pages:
            if os.path.exists(page["output_dir"]):
                shutil.rmtree(page["output_dir"])

    def preprocess_pages(self, pages):
        result = []

        # preprocess page url and output path
        for page in pages:
            file_name, file_ext = os.path.splitext(page["file_path"])
            output_name = os.path.basename(file_name) + ".html"
            output_path = os.path.join(page["output_dir"], output_name)

            page["url"] = "/" + output_path
            page["output_path"] = output_path

            if not os.path.exists(page["output_dir"]):
                os.makedirs(page["output_dir"])

            result.append(page)

        return result

    def generate_pages(self):
        # generate and output pages
        for page in self.pages:
            # create pages output dir
            if not os.path.exists(page["output_dir"]):
                os.makedirs(page["output_dir"])

            # generate page
            print "-> " + page["output_path"]
            template = self.env.get_template(page["template"])
            page_content = self.convert_md(page["file_path"])
            page_name = os.path.basename(os.path.splitext(page["file_path"])[0])
            html = template.render(
                pages=self.pages,
                page_content=page_content,
                page_name=page_name
            )
            output_file = open(page["output_path"], "w")
            output_file.write(html)
            output_file.close()

    def generate_index(self):
        template = self.env.get_template(self.index_template)
        with open("index.html", "w") as output_page:
            print "-> index.html"
            page = template.render(posts=self.posts, pages=self.pages)
            output_page.write(page)
            output_page.close()

    def generate_posts(self):
        # pre-check
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # generate posts
        for post in self.posts:
            print "-> " + post.output_path

            # render template
            template = self.env.get_template(self.post_template)
            post_html = self.convert_md(post.file_path)
            html = template.render(post=post_html, pages=self.pages)

            # fix internal links
            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("a")
            for link in links:
                is_digit = os.path.basename(link["href"])[0:6].isdigit()
                no_ext = os.path.splitext(link["href"])[1] is ""
                if is_digit and no_ext:
                    link["href"] += ".html"
            html = str(soup)

            # output post
            post_file = open(post.output_path, "w")
            post_file.write(html)
            post_file.close()

    def run(self):
        self.purge_dirs()
        self.copy_dir()
        self.generate_pages()
        self.generate_index()
        self.generate_posts()
