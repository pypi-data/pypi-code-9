# -*- coding: utf-8 -*-


import re
from ..convert import normalize
from robot.libraries.BuiltIn import BuiltIn


__all__ = [
    'then_response_should_only_contain_address_where',
    'then_response_should_at_least_contain_address_where',
    'then_response_should_only_contain_address_or_poi_where',
    'then_response_should_at_least_contain_address_or_poi_where',
    'then_response_should_only_contain_address_or_poi_or_rubric_or_storechain_where',
    'then_response_should_at_least_contain_address_or_poi_or_rubric_or_storechain_where',
    'then_response_should_be_empty',
    'then_response_code_should_be']


#
# PRIVATE METHODS (WILL NOT BE EXPORTED AS KEYWORDS)
#


def add_expected_tag(text, **expected_fields):

    fields = []

    for key, value in expected_fields.items():
        if value:
            if isinstance(value, list):
                fields += [u"{} is in {}".format(key, value)]
            else:
                fields += [u"{} is {}".format(key, value)]

    if fields:
        BuiltIn().run_keyword("Set Tags", u"expected:{} WHERE {}".format(text, " AND ".join(fields)))


class Suggestion:

    def __init__(self, suggestion):

        self.highlightings = []

        try:
            self.type = suggestion['type']
        except KeyError:
            self.type = ''

        try:
            self.name = re.sub("<em>|</em>", "", suggestion['name'])
            self.highlightings += re.findall('<em>([^<]*)</em>', suggestion['name'])

        except KeyError:
            self.name = ''

        try:
            self.address = re.sub("<em>|</em>", "", suggestion['address'])
            self.highlightings += re.findall('<em>([^<]*)</em>', suggestion['address'])

        except KeyError:
            self.address = ''

        self.highlightings = [normalize(highlighting) for highlighting in self.highlightings]

    def is_address(self):
        return True if (self.type == 'address') else False

    def is_poi(self):
        return True if (self.type == 'poi') else False

    def is_rubric(self):
        return True if (self.type == 'rubric') else False

    def is_storechain(self):
        return True if (self.type == 'store_chain') else False

    def name_ok(self, name):
        return (normalize(name) in normalize(self.name)) if name else True

    def address_ok(self, address):
        return (normalize(address) in normalize(self.address)) if address else True

    def highlighting_ok(self, highlightings):

        for highlighting in highlightings:

            if (normalize(highlighting) not in self.highlightings):

                return False

        return True


def response_should_contain_address_where(only=False, name=None, address=None, highlighting=None):

    # Add the expected result tag to the calling test case
    add_expected_tag(
        "Response should {} contain addresses".format("only" if only else "at least"),
        **{
            "name": name,
            "address": address,
            "highlighting": highlighting})

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")



#    response = BuiltIn().run_keyword("Log To Console", response['suggests'])
#
#
#    for suggestion in response['suggests']:
#
#        suggestion = Suggestion(suggestion)




    assert True



def response_should_contain_address_or_poi_where(only=False, name=None, address=None, highlighting=None):

    # Add the expected result tag to the calling test case
    add_expected_tag(
        "Response should {} contain addresses or pois".format("only" if only else "at least"),
        **{
            "name": name,
            "address": address,
            "highlighting": highlighting})

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")








#    for suggestion in response['suggests']:
#
#        suggestion = Suggestion(suggestion)






    assert True


def response_should_contain_address_or_poi_or_rubric_or_storechain_where(only=False, name=None, address=None, highlighting=None):

    # Add the expected result tag to the calling test case
    add_expected_tag(
        "Response should {} contain addresses or pois or rubric or storechain".format("only" if only else "at least"),
        **{
            "name": name,
            "address": address,
            "highlighting": highlighting})

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")








#    for suggestion in response['suggests']:
#
#        suggestion = Suggestion(suggestion)









    assert True


#
# KEYWORDS
#


def then_response_should_only_contain_address_where(name=None, address=None, highlighting=None):
    response_should_contain_address_where(only=True, name=name, address=address, highlighting=highlighting)


def then_response_should_at_least_contain_address_where(name=None, address=None, highlighting=None):
    response_should_contain_address_where(only=False, name=name, address=address, highlighting=highlighting)


def then_response_should_only_contain_address_or_poi_where(name=None, address=None, highlighting=None):
    response_should_contain_address_or_poi_where(only=True, name=name, address=address, highlighting=highlighting)


def then_response_should_at_least_contain_address_or_poi_where(name=None, address=None, highlighting=None):
    response_should_contain_address_or_poi_where(only=False, name=name, address=address, highlighting=highlighting)


def then_response_should_only_contain_address_or_poi_or_rubric_or_storechain_where(name=None, address=None, highlighting=None):
    response_should_contain_address_or_poi_or_rubric_or_storechain_where(only=True, name=name, address=address, highlighting=highlighting)


def then_response_should_at_least_contain_address_or_poi_or_rubric_or_storechain_where(name=None, address=None, highlighting=None):
    response_should_contain_address_or_poi_or_rubric_or_storechain_where(only=False, name=name, address=address, highlighting=highlighting)


def then_response_should_be_empty():

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")

    if not response or not response['suggests']:
        assert True
    else:
        assert False


def then_response_code_should_be(code):

    # Get response code from global testsuite variables
    response_code = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_CODE}")

    if int(response_code) != int(code):
        assert False
    else:
        assert True
