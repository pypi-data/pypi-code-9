# -*- coding: utf-8 -*-


import re
import urllib2
from robot.libraries.BuiltIn import BuiltIn


class Environment:

    search_urls = {
        "snapshot": "http://search.mappysnap.net",
        "recette": "http://search.mappyrecette.net",
        "pproduction": "http://search.mappypp.net",
        "production": "http://search.mappy.net"}

    suggest_urls = {
        "snapshot": "http://suggest.mappysnap.net",
        "recette": "http://suggest.mappyrecette.net",
        "pproduction": "http://suggest.mappypp.net",
        "production": "http://suggest.mappy.net"}

    solr_pois_url = ""

    def __init__(self, environment=None):
        """
            Environment is a target ('snapshot', 'recette', 'pproduction', 'production') with an optional version separated with ':'.
            Default version is '1.0'.
            If environment is not specified by parameters, it's retrieved from Robot Framework global variables.
            Ex. : snapshot:1.0
                  recette:1.1
                  snapshot (same as snapshot:1.0)
        """

        # Default version
        self.version = '1.0'

        # Get environment from Robot Framework global variables if not specified in constructor arguments
        if not environment:
            environment = BuiltIn().run_keyword("Get Variable Value", "${ENVIRONMENT}")

        self.target = environment.split(':')[0]

        # Get version from environment
        try:
            self.version = environment.split(':')[1]
        except IndexError:
            pass

        # Get solr pois base URL
        if not Environment.solr_pois_url:
            try:
                response = urllib2.urlopen(Environment.search_urls[self.target.lower()])
                match = re.search("Hostname\s*:\s*(\S*?)\s*<br>", response.read())
                response.close()

                if match:
                    Environment.solr_pois_url = u"http://{}:8080/solr/pois".format(match.group(1))
            except:
                Environment.solr_pois_url = ""

    def get(self):
        """
            Retrieve environment
        """
        return u"{}:{}".format(self.target, self.version)

    def search(self):
        """
            Retrieve search service base URL
        """
        return u"{}/search/{}".format(Environment.search_urls[self.target.lower()], self.version)

    def suggest(self):
        """
            Retrieve suggest service base URL
        """
        return u"{}/suggest/{}".format(Environment.suggest_urls[self.target.lower()], self.version)

    def solr_pois(self):
        """
            Retrieve pois solr core base URL
        """
        return Environment.solr_pois_url
