#!/usr/bin/python
"""A script to scrape Amazon product reviews

    Copyright 2014 Herman Tai

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse
import logging
import os
import random
import sys
import time
import urllib
import urlparse

import requests
from lxml import html

from sorno import loggingutil


_LOG = logging.getLogger(__name__)
_PLAIN_LOGGER = None  # will be created in main()


class App(object):
    def __init__(self, url):
        self.url = url

    def run(self):
        _LOG.info("Given url: %s", self.url)
        url, cur_page_num = self.get_main_url_and_page_number(self.url)
        _LOG.info("Main url: %s", url)

        _LOG.info("Fetch page %d", cur_page_num)
        initial_page_tree = self.get_tree_from_url(url)

        prev_page_items = None
        cur_page_items = self.get_items_from_page_tree(initial_page_tree)
        all_items = list(cur_page_items)

        while prev_page_items != cur_page_items:
            # sleep a little bit to avoid being characterized as a bot
            time.sleep(random.uniform(0.5, 2))

            prev_page_items = cur_page_items
            cur_page_num += 1
            new_url = url + "&pageNumber=" + str(cur_page_num)
            _LOG.info("Fetch page %s", cur_page_num)
            cur_page_items = self.get_items_from_page_tree(
                self.get_tree_from_url(new_url)
            )

            all_items.extend(cur_page_items)

        for item in all_items:
            print(item.encode('utf8'))
            print("-" * 70)

    def get_main_url_and_page_number(self, url):
        n = 1
        parsed = urlparse.urlparse(url)

        query = parsed.query
        query_list = urlparse.parse_qsl(query)
        modified_query_list = []
        # capture the pageNumber in query, and leave other as is
        for k, v in query_list:
            if k == "pageNumber":
                n = int(v)
            else:
                modified_query_list.append((k, v))
        modified_query = urllib.urlencode(modified_query_list)

        modified_parsed = urlparse.ParseResult(
            scheme=parsed.scheme,
            netloc=parsed.netloc,
            path=parsed.path,
            params=parsed.params,
            query=modified_query,
            fragment=parsed.fragment,
        )
        return modified_parsed.geturl(), n

    def get_tree_from_url(self, url):
        website_text = requests.get(url).text
        return html.fromstring(website_text)

    def get_items_from_page_tree(self, tree):
        reviews = self.get_reviews_from_node(tree)
        return [
            self.get_text_from_element(review_element)
            for review_element in reviews
        ]

    def get_reviews_from_node(self, node):
        reviews = node.xpath("//span[@class='a-size-base review-text']")
        return reviews

    def get_text_from_element(self, node):
        """
        Return a plain text representation of an html node.
        """
        text_segments = []
        self._collect_text_from_element(node, text_segments)
        return "".join(text_segments)

    def _collect_text_from_element(self, node, text_segments):
        """
        Collect text from node and all its children recursively and put into
        text_segments as a list of strings.
        """
        if node.tag.lower() == "br":
            text_segments.append(os.linesep)

        if node.text:
            text_segments.append(node.text)

        for child in node:
            self._collect_text_from_element(child, text_segments)

        if node.tail:
            text_segments.append(node.tail)


def parse_args(cmd_args):
    description = """
A script to scrape Amazon product reviews
    """
    parser = argparse.ArgumentParser(
        description=description,
        # formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
    )
    parser.add_argument(
        "url",
        help="The url that point to all reviews of an Amazon product. You"
            + " probably want to single-quote the url when running this"
            + " script in the command line because the url probably contains"
            + " shell characters. An example of a url is:"
            + " http://www.amazon.com/Ito-En-Beverage-Unsweetened-Bottles/product-reviews/B0017T2MWW/ref=cm_cr_dp_see_all_summary?ie=UTF8&showViewpoints=1&sortBy=byRankDescending",
    )

    args = parser.parse_args(cmd_args)
    return args


def main():
    global _PLAIN_LOGGER

    args = parse_args(sys.argv[1:])

    loggingutil.setup_logger(_LOG, debug=args.debug)
    _PLAIN_LOGGER = loggingutil.create_plain_logger("PLAIN")

    app = App(args.url)
    app.run()


if __name__ == '__main__':
    main()
