# -*- coding: utf-8 -*-


import json
import re
from environment import Environment
from robot.libraries.BuiltIn import BuiltIn
from lbs2.testing import HTTPTestCaseMixIn
from tornado.escape import url_escape


__all__ = [
    'when_i_search',
    'when_i_want_a_suggestion',
    'when_i_search_the_first_suggestion']


def when_i_search(searched, bbox="45.207962083566905,-3.252314814814789,49.57272451543066,7.569444444444459", extend_bbox=1, filter="places", language="FRE", favorite_country="250", maximum_results=100):
    """
        Searches through Mappy's search API
    """

    # Format Base URL
    base_url = Environment().search()

    # Format URI
    uri = u"/find?q={}&bbox={}&extend_bbox={}&f={}&language={}&favorite_country={}&max_results={}&loc_format=geojson".format(
        url_escape(searched),
        bbox,
        extend_bbox,
        filter,
        language,
        favorite_country,
        maximum_results).encode('utf-8')

    # Add some tags to the calling test case
    BuiltIn().run_keyword("Set Tags", u"environment:{}".format(Environment().get()))
    BuiltIn().run_keyword("Set Tags", u"base_url:{}".format(base_url))
    BuiltIn().run_keyword("Set Tags", u"uri:{}".format(uri))
    BuiltIn().run_keyword("Set Tags", u"searched:{}".format(searched))

    # Send request
    try:
        response = HTTPTestCaseMixIn().fetch("{}{}".format(base_url, uri))

        # Return the response code as a global test case variable
        BuiltIn().run_keyword("Set Test Variable", "${RESPONSE_CODE}", response.getcode())

        # Return the response body as a global test case variable
        BuiltIn().run_keyword("Set Test Variable", "${RESPONSE_BODY}", json.loads(response.body))

    except Exception as e:

        # Return the response code as a global test case variable
        BuiltIn().run_keyword("Set Test Variable", "${RESPONSE_CODE}", e.getcode())


def when_i_want_a_suggestion(searched, bbox="45.207962083566905,-3.252314814814789,49.57272451543066,7.569444444444459", filter="places"):
    """
        Searches through Mappy's suggest API
    """

    # Format Suggest Base URL
    base_url_suggest = Environment().suggest()

    # Format Suggest URI
    uri_suggest = u"/suggest?bbox={}&q={}&f={}".format(bbox, url_escape(searched), filter).encode('utf-8')

    # Add some tags to the calling test case
    BuiltIn().run_keyword("Set Tags", u"environment:{}".format(Environment().get()))
    BuiltIn().run_keyword("Set Tags", u"base_url:{}".format(base_url_suggest))
    BuiltIn().run_keyword("Set Tags", u"uri:{}".format(uri_suggest))
    BuiltIn().run_keyword("Set Tags", u"searched:{}".format(searched))

    # Send request
    try:
        response = HTTPTestCaseMixIn().fetch("{}{}".format(base_url_suggest, uri_suggest))

        # Return the response code as a global test case variable
        BuiltIn().run_keyword("Set Test Variable", "${RESPONSE_CODE}", response.getcode())

        # Return the response body as a global test case variable
        BuiltIn().run_keyword("Set Test Variable", "${RESPONSE_BODY}", json.loads(response.body))

    except Exception as e:

        # Return the response code as a global test case variable
        BuiltIn().run_keyword("Set Test Variable", "${RESPONSE_CODE}", e.getcode())


def when_i_search_the_first_suggestion(searched, bbox):
    """
        Searches through Mappy's suggest then search APIs
    """

    # Format Suggest Base URL
    base_url_suggest = Environment().suggest()

    # Format Suggest URI
    uri_suggest = u"/suggest?bbox={}&q={}&f=all".format(bbox, url_escape(searched)).encode('utf-8')

    # Add some tags to the calling test case
    BuiltIn().run_keyword("Set Tags", u"environment:{}".format(Environment().get()))
    BuiltIn().run_keyword("Set Tags", u"base_url:{}".format(base_url_suggest))
    BuiltIn().run_keyword("Set Tags", u"uri:{}".format(uri_suggest))
    BuiltIn().run_keyword("Set Tags", u"searched:{}".format(searched))

    try:
        # Send request to suggest
        response_body = HTTPTestCaseMixIn().fetch("{}{}".format(base_url_suggest, uri_suggest)).body
        response_json = json.loads(response_body)

        # Send first suggestion to search
        if 'suggests' in response_json and response_json['suggests']:

            # Format Search Base URL
            base_url_search = Environment().search()

            # Get first suggestion without Solr highlighter tags
            first_name = re.sub("<em>|</em>", "", response_json['suggests'][0]['name']) if 'name' in response_json['suggests'][0] else ""
            first_address = re.sub("<em>|</em>", "", response_json['suggests'][0]['address']) if 'address' in response_json['suggests'][0] else ""
            first_suggestion = (u"{} {}".format(first_name, first_address)).strip()

            # Format Search URI
            uri_search = u"/find?extend_bbox=1&bbox={}&q={}&favorite_country=250&language=FRE&loc_format=geojson&max_results=100".format(bbox, url_escape(first_suggestion)).encode('utf-8')

            # Send request to search
            response_body = HTTPTestCaseMixIn().fetch("{}{}".format(base_url_search, uri_search)).body
            response_json = json.loads(response_body)

            # Return the response as a global test case variable
            BuiltIn().run_keyword("Set Test Variable", "${RESPONSE_BODY}", response_json)

        else:
            assert (False), "Empty response from suggest"

    except Exception as e:
        assert (False), str(e)
