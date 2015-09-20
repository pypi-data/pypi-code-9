#!/usr/bin/python
import sys
import os
import logging
from optparse import OptionParser
from io import StringIO
import json
import locale

from lxml import etree
from lxml.etree import ParserError
from lxml.etree import XMLSyntaxError
import requests
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from requests.exceptions import Timeout
from requests.exceptions import ReadTimeout

import xpathExpressions
from version import __version__


class PlayListingScraper(object):
    log = logging.getLogger("play_listing_scraper")
    # The logger's level must be set to the "lowest" level.
    log.setLevel(logging.DEBUG)
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    def parse_tree(self, tree, package_name, version_code, out_dir):
        title = self.get_property(tree, xpathExpressions.TITLE)
        description = self.get_property(tree, xpathExpressions.DESCRIPTION)
        category = self.get_property(tree, xpathExpressions.CATEGORY)
        price = self.get_property(tree, xpathExpressions.PRICE)
        if len(price) > 1:
            price = price.split(' ')[1]
        date_published = self.get_property(tree,
                                           xpathExpressions.DATE_PUBLISHED)
        os_version = self.get_property(tree, xpathExpressions.OPERATING_SYSTEM)
        rating_count_text = self.get_property(tree,
                                              xpathExpressions.RATING_COUNT)
        rating_count = 0
        if rating_count_text != '':
            rating_count = locale.atoi(rating_count_text)

        rating_text = self.get_property(tree, xpathExpressions.RATING)
        rating = 0
        if rating_text != '':
            rating = float(rating_text.split()[1])
        content_rating = self.get_property(tree,
                                           xpathExpressions.CONTENT_RATING)
        creator = self.get_property(tree, xpathExpressions.CREATOR)
        creator_url = self.get_property(tree, xpathExpressions.CREATOR_URL)
        creator_address = self.get_property(tree,
                                            xpathExpressions.CREATOR_ADDRESS)
        install_size = self.get_property(tree, xpathExpressions.INSTALL_SIZE)
        download_count_text = self.get_property(tree,
                                                xpathExpressions.DOWNLOAD_COUNT_TEXT)
        download_count = 0
        if download_count_text != '':
            download_count = locale.atoi(download_count_text.split("-")[0].strip())
        privacy_url = self.get_property(tree, xpathExpressions.PRIVACY_URL)
        whats_new = self.get_property(tree, xpathExpressions.WHATS_NEW)

        app = json.dumps({"n": package_name,
                          "verc": version_code,
                          "t": title,
                          "desc": description,
                          "cat": category,
                          "pri": price,
                          "dtp": date_published,
                          "os": os_version,
                          "rct": rating_count,
                          "rate": rating,
                          "crat": content_rating,
                          "crt": creator,
                          "cadd": creator_address,
                          "curl": creator_url,
                          "sz": install_size,
                          "dct": download_count,
                          "dtxt": download_count_text,
                          "purl": privacy_url,
                          "new": whats_new
                          }, sort_keys=True, indent=4, separators=(',', ': '))
        out_file = os.path.join(out_dir, package_name + '-' + version_code +
                                '.listing.json')
        with open(out_file, 'w') as f:
            f.write(app)
        self.log.info("Listing details info has been written at %s", out_file)

    @staticmethod
    def get_property(tree, xpath_expressions):
        val = None
        for exp in xpath_expressions:
            val = tree.xpath(exp)
            if val:
                break
        return ' '.join(val).strip()

    def scrape_content(self, html_content, package_name, version_code,
                       out_dir=os.getcwd()):
        try:
            parser = etree.HTMLParser()
            tree = etree.parse(html_content, parser)
            if tree.getroot() is None:
                self.log.error("Invalid html content")
            else:
                self.parse_tree(tree, package_name, version_code, out_dir)
        except (ParserError, XMLSyntaxError) as e:
            self.log.error("Error in parsing html page for %s message: %s",
                           package_name + "-" + version_code, e)

    def scrape_remote_page(self, package_name, version_code,
                           out_dir=os.getcwd()):
        try:
            play_url = "https://play.google.com/store/apps/details?id=" + \
                       package_name
            r = requests.get(play_url)
            if r.status_code == 200:
                html_content = StringIO(requests.get(play_url).text)
                self.scrape_content(html_content, package_name, version_code,
                                    out_dir)
            else:
                self.log.error("Failed to request the html page for %s " +
                               "http request status code: %i", package_name,
                               r.status_code)
        except (ConnectionError, HTTPError, Timeout, ReadTimeout) as e:
            self.log.error("Network error while requesting the html page for" +
                           " %s message: %s",
                           package_name + "-" + version_code, e)

    def cli(self, argv):
        out_dir = os.getcwd()
        logging_file = None
        logging_level = logging.ERROR
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        # Create console logger and set its formatter and level
        logging_console = logging.StreamHandler(sys.stdout)
        logging_console.setFormatter(formatter)
        logging_console.setLevel(logging.DEBUG)
        # Add the console logger
        self.log.addHandler(logging_console)
        parser = OptionParser(
            usage="%prog [options] " +
                  "packageName-versionCode | google_play_html_page_file",
            version="%prog " + __version__,
            description="A tool for Scraping an app's listing details data " +
                        "from the Google Play Store store " +
                        "and saving it in a file in JSON format.")
        parser.add_option("-o", "--out-dir", dest="out_dir",
                          help="write out file to a target directory." +
                               " Default is current directory", metavar="DIR")
        parser.add_option("-l", "--log", dest="log_file",
                          help="write logs to FILE.", metavar="FILE")
        parser.add_option('-v', '--verbose', dest="verbose", default=0,
                          action='count', help='Increase verbosity.')
        (options, args) = parser.parse_args(argv)
        if len(args) != 1:
            parser.error("incorrect number of arguments.")
        if options.out_dir:
            if os.path.isdir(options.out_dir):
                out_dir = os.path.abspath(options.out_dir)
            else:
                parser.error("Invalid output directory.")
        if options.log_file:
            logging_file = logging.FileHandler(options.log_file, mode='a',
                                               encoding='utf-8', delay=False)
            logging_file.setLevel(logging_level)
            logging_file.setFormatter(formatter)
            self.log.addHandler(logging_file)
        if options.verbose:
            levels = [logging.ERROR, logging.INFO, logging.DEBUG]
            logging_level = levels[min(len(levels) - 1, options.verbose)]
        if logging_file:
            logging_file.setLevel(logging_level)
        if os.path.isfile(args[0]):
            app = os.path.basename(args[0]).split("-")
            if len(app) != 2:
                self.log.error("The html file must be named as " +
                               "packageName-versionCode.html")
                return
            package_name = app[0]
            version_code = app[1].split('.')[0]
            html_file = os.path.abspath(args[0])
            self.scrape_content(html_file, package_name, version_code, out_dir)

        elif "-" in args[0]:
            self.scrape_remote_page(args[0].split('-')[0],
                                    args[0].split('-')[1], out_dir)
        else:
            self.log.error('Invalid app name or html file path. ' +
                           'Arguments must be either packageName-versionCode ' +
                           'or a valid path name.')


def playlistingscraper_command():
    PlayListingScraper().cli(sys.argv[1:])


if __name__ == '__main__':
    playlistingscraper_command()
