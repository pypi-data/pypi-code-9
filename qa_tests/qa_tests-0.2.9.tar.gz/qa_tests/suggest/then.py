# -*- coding: utf-8 -*-


import json
import urllib2
from tornado.escape import url_escape
from convert import normalize
from environment import Environment
from robot.libraries.BuiltIn import BuiltIn


__all__ = [
    'then_response_should_only_contain_pois_where',
    'then_response_should_at_least_contain_pois_where',
    'then_response_should_only_contain_landmarks_where',
    'then_response_should_at_least_contain_landmarks_where',
    'then_response_should_only_contain_addresses_where',
    'then_response_should_at_least_contain_addresses_where',
    'then_response_should_only_contain_addresses_and_pois_where',
    'then_response_should_at_least_contain_addresses_and_pois_where',
    'then_response_should_be_inside',
    'then_response_should_be_outside',
    'then_response_should_be_empty',
    'then_response_code_should_be',
    'then_response_should_contain']


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


class Address:

    def __init__(self, address):

        try:
            self.geocode_level = address['properties']['geocode_level']
        except KeyError:
            self.geocode_level = ''

        try:
            self.name = address['properties']['formatted_address']['split_label'][0]
        except KeyError:
            self.name = ''

        try:
            self.way_number = address['properties']['address_components']['way_number']
        except KeyError:
            self.way_number = ''

        try:
            self.way = address['properties']['address_components']['way']
        except KeyError:
            self.way = ''

        try:
            if isinstance(address['properties']['address_components']['postcode'], list):
                self.postal_codes = address['properties']['address_components']['postcode']
            else:
                self.postal_codes = address['properties']['address_components']['postcode'].split(' - ')
        except KeyError:
            self.postal_codes = []

        try:
            self.town_name = address['properties']['address_components']['town']['label']
        except KeyError:
            self.town_name = ''

        try:
            self.country_code = address['properties']['address_components']['country']['code'].lstrip('0')
        except KeyError:
            self.country_code = ''

        try:
            self.country_name = address['properties']['address_components']['country']['label']
        except KeyError:
            self.country_name = ''

        try:
            self.latitude = float(address['geometry']['geometries'][0]['coordinates'][1])
        except KeyError:
            self.latitude = None

        try:
            self.longitude = float(address['geometry']['geometries'][0]['coordinates'][0])
        except KeyError:
            self.longitude = None

    def is_landmark(self):
        return True if (self.geocode_level == 'landmark') else False

    def name_ok(self, name):
        return (normalize(self.name).startswith(normalize(name))) if name else True

    def way_number_ok(self, way_number):
        return (self.way_number == way_number) if way_number else True

    def way_ok(self, way):
        return (normalize(self.way) == normalize(way)) if way else True

    def postal_codes_ok(self, postal_codes):
        return (len([postal_code for postal_code in self.postal_codes if (postal_code in postal_codes)]) > 0) if postal_codes else True

    def town_name_ok(self, town_name):
        return (normalize(self.town_name) == normalize(town_name)) if town_name else True

    def country_code_ok(self, country_code):
        return (self.country_code == country_code.lstrip('0')) if country_code else True

    def country_name_ok(self, country_name):
        return (self.country_name == country_name) if country_name else True

    def is_in_bbox(self, bbox):

        bbox = bbox.split(',')
        bbox_south_west_longitude = float(bbox[1])
        bbox_south_west_latitude = float(bbox[0])
        bbox_north_est_longitude = float(bbox[3])
        bbox_north_est_latitude = float(bbox[2])

        # Latitude comparison in France
        if (self.latitude < bbox_south_west_latitude) and (self.latitude > bbox_north_est_latitude):
            return False

        # Longitude comparison in France
        if (self.longitude < bbox_south_west_longitude) or (self.longitude > bbox_north_est_longitude):
            return False

        return True


class Poi:

    def __init__(self, poi):

        try:
            self.id = poi['id']
        except KeyError:
            self.id = ''

        try:
            self.name = poi['name']
        except KeyError:
            self.name = ''

        try:
            self.way_number = poi['houseNumber']
        except KeyError:
            self.way_number = ''

        try:
            self.way = poi['street']
        except KeyError:
            self.way = ''

        try:
            self.postal_codes = poi['pCode']
            if not isinstance(self.postal_codes, list):
                self.postal_codes = [self.postal_codes]
        except KeyError:
            self.postal_codes = []

        try:
            self.town_code = poi['townCode']
        except KeyError:
            self.town_code = ''

        try:
            self.town_name = poi['town']
        except KeyError:
            self.town_name = ''

        try:
            self.rubric_ids = [rubric['id'] for rubric in poi['allRubrics']]
        except KeyError:
            self.rubric_ids = []

        try:
            self.country_name = poi['country']
        except KeyError:
            self.country_name = ''

        try:
            self.latitude = float(poi['lat'])
        except KeyError:
            self.latitude = None

        try:
            self.longitude = float(poi['lng'])
        except KeyError:
            self.longitude = None

    def name_ok(self, name):
        return (normalize(name) in normalize(self.name)) if name else True

    def way_number_ok(self, way_number):
        return (self.way_number == way_number) if way_number else True

    def way_ok(self, way):
        return (normalize(self.way) == normalize(way.replace(self.way_number, "", 1))) if way else True

    def postal_codes_ok(self, postal_codes):
        return (len([postal_code for postal_code in self.postal_codes if (postal_code in postal_codes)]) > 0) if postal_codes else True

    def town_code_ok(self, town_code):
        return (self.town_code == town_code) if town_code else True

    def town_name_ok(self, town_name):
        return (normalize(self.town_name) == normalize(town_name)) if town_name else True

    def rubric_ids_ok(self, rubric_ids):
        return (len([rubric_id for rubric_id in self.rubric_ids if (rubric_id in rubric_ids)]) > 0) if rubric_ids else True

    def storechain_ids_ok(self, storechain_ids):
        if storechain_ids:
            base_url = Environment().solr_pois()
            storechains = url_escape(u'("{}")'.format(u'" OR "'.join(storechain_ids)))
            url = u"{}/select?q=id:{}&fq=store_chains_id:{}&wt=json&fl=numFound".format(base_url, self.id, storechains)
            response = urllib2.urlopen(url)
            response_json = json.loads(response.read())
            response.close()
            return (int(response_json["response"]["numFound"]) >= 1)
        else:
            return True

    def country_name_ok(self, country_name):
        return (self.country_name == country_name) if country_name else True

    def is_in_bbox(self, bbox):

        bbox = bbox.split(',')
        bbox_south_west_longitude = float(bbox[1])
        bbox_south_west_latitude = float(bbox[0])
        bbox_north_est_longitude = float(bbox[3])
        bbox_north_est_latitude = float(bbox[2])

        # Latitude comparison in France
        if (self.latitude < bbox_south_west_latitude) and (self.latitude > bbox_north_est_latitude):
            return False

        # Longitude comparison in France
        if (self.longitude < bbox_south_west_longitude) or (self.longitude > bbox_north_est_longitude):
            return False

        return True


def response_should_contain_pois_where(only=False, name=None, way=None, postal_codes=None, town_code=None, town_name=None, rubric_ids=None, storechain_ids=None):

    # Add the expected result tag to the calling test case
    add_expected_tag(
        "Response should {} contain pois".format("only" if only else "at least"),
        **{
            "name": name,
            "way": way,
            "postal code": postal_codes,
            "town code": town_code,
            "town name": town_name,
            "rubric": rubric_ids,
            "store chain": storechain_ids})

    # Get response from global testsuite variable
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")

    if only:
        assert ('addresses' not in response), u"Response should not contain address"

    if 'pois' in response:

        poi_ok = False

        for element in response['pois']:

            poi = Poi(element)

            # Check current POI
            try:
                assert poi.name_ok(name), u"Wrong name in '{}'".format(poi.name)
                assert poi.way_ok(way), u"Wrong way in '{}'".format(poi.name)
                assert poi.postal_codes_ok(postal_codes), u"Wrong postal codes in '{}'".format(poi.name)
                assert poi.town_code_ok(town_code), u"Wrong town code in '{}'".format(poi.name)
                assert poi.town_name_ok(town_name), u"Wrong town name in '{}'".format(poi.name)
                assert poi.rubric_ids_ok(rubric_ids), u"Wrong rubric ids in '{}'".format(poi.name)
                assert poi.storechain_ids_ok(storechain_ids), u"Wrong store chain in '{}'".format(poi.name)
                poi_ok = True

                # If response should at least contain the expected poi and this poi is found
                if not only:
                    break

            except AssertionError, e:
                if only:
                    raise e
                else:
                    pass

        assert (poi_ok), u"Expected poi not found"

    else:
        assert (False), u"Response doesn't contain any poi"


def response_should_contain_landmarks_where(only=False, name=None, postal_codes=None, town_name=None, country_code=None, country_name=None):

    # Add the expected result tag to the calling test case
    add_expected_tag(
        "Response should {} contain landmarks".format("only" if only else "at least"),
        **{
            "name": name,
            "postal code": postal_codes,
            "town name": town_name,
            "country code": country_code,
            "country name": country_name})

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")

    if only:
        assert ('pois' not in response), u"Response should not contain poi"

    if 'addresses' in response:

        landmark_ok = False

        for element in response['addresses']['features']:

            address = Address(element)

            # Check current landmark
            try:
                assert address.is_landmark(), u"'{}' is not a landmark".format(address.name)
                assert address.name_ok(name), u"Wrong name in '{}'".format(address.name)
                assert address.postal_codes_ok(postal_codes), u"Wrong postal codes in '{}'".format(address.name)
                assert address.town_name_ok(town_name), u"Wrong town name in '{}'".format(address.name)
                assert address.country_code_ok(country_code), u"Wrong country code in '{}'".format(address.name)
                assert address.country_name_ok(country_name), u"Wrong country name in '{}'".format(address.name)
                landmark_ok = True

                # If response should at least contain the expected landmark and this landmark is found
                if not only:
                    break

            except AssertionError, e:
                if only:
                    raise e
                else:
                    pass

        assert landmark_ok, u"Expected landmark not found"

    else:
        assert False, u"Response doesn't contain any landmark"


def response_should_contain_addresses_where(only=False, name=None, way_number=None, way=None, postal_codes=None, town_name=None, country_code=None, country_name=None):

    # Add the expected result tag to the calling test case
    add_expected_tag(
        "Response should {} contain addresses".format("only" if only else "at least"),
        **{
            "name": name,
            "way number": way_number,
            "way": way,
            "postal code": postal_codes,
            "town name": town_name,
            "country code": country_code,
            "country name": country_name})

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")

    if only:
        assert ('pois' not in response), u"Response should not contain poi"

    if 'addresses' in response:

        address_ok = False

        for element in response['addresses']['features']:

            address = Address(element)

            # Check current address
            try:
                assert address.name_ok(name), u"Wrong name in '{}'".format(address.name)
                assert address.way_number_ok(way_number), u"Wrong way number in '{}'".format(address.name)
                assert address.way_ok(way), u"Wrong way in '{}'".format(address.name)
                assert address.postal_codes_ok(postal_codes), u"Wrong postal codes in '{}'".format(address.name)
                assert address.town_name_ok(town_name), u"Wrong town name in '{}'".format(address.name)
                assert address.country_code_ok(country_code), u"Wrong country code in '{}'".format(address.name)
                assert address.country_name_ok(country_name), u"Wrong country name in '{}'".format(address.name)
                address_ok = True

                # If response should at least contain the expected address and this address is found
                if not only:
                    break

            except AssertionError, e:
                if only:
                    raise e
                else:
                    pass

        assert address_ok, u"Expected address not found"

    else:
        assert False, u"Response doesn't contain any address"


def response_should_contain_addresses_and_pois_where(only=False, way_number=None, way=None, postal_codes=None, town_name=None, country_name=None):

    # Add the expected result tag to the calling test case
    add_expected_tag(
        "Response should {} contain addresses and pois".format("only" if only else "at least"),
        **{
            "way number": way_number,
            "way": way,
            "postal code": postal_codes,
            "town name": town_name,
            "country name": country_name})

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")

    if 'addresses' in response:

        address_ok = False

        for element in response['addresses']['features']:

            address = Address(element)

            # Check current address
            try:
                assert address.way_number_ok(way_number), u"Wrong way number in address '{}'".format(address.name)
                assert address.way_ok(way), u"Wrong way in address '{}'".format(address.name)
                assert address.postal_codes_ok(postal_codes), u"Wrong postal codes in address '{}'".format(address.name)
                assert address.town_name_ok(town_name), u"Wrong town name in address '{}'".format(address.name)
                assert address.country_name_ok(country_name), u"Wrong country name in address '{}'".format(address.name)
                address_ok = True

                # If response should at least contain the expected address and this address is found
                if not only:
                    break

            except AssertionError, e:
                if only:
                    raise e
                else:
                    pass

        assert address_ok, u"Expected address not found"

        if 'pois' in response:

            for element in response['pois']:

                poi = Poi(element)

                # Check current POI
                assert poi.way_number_ok(way_number), u"Wrong way number in poi '{}'".format(poi.name)
                assert poi.way_ok(way), u"Wrong way in poi '{}'".format(poi.name)
                assert poi.postal_codes_ok(postal_codes), u"Wrong postal codes in poi '{}'".format(poi.name)
                assert poi.town_name_ok(town_name), u"Wrong town name in poi '{}'".format(poi.name)
                assert poi.country_name_ok(country_name), u"Wrong country name in poi '{}'".format(poi.name)

    else:
        assert False, u"Response doesn't contain any address"


#
# KEYWORDS
#


def then_response_should_only_contain_pois_where(name=None, way=None, postal_codes=None, town_code=None, town_name=None, rubric_ids=None, storechain_ids=None):
    response_should_contain_pois_where(only=True, name=name, way=way, postal_codes=postal_codes, town_code=town_code, town_name=town_name, rubric_ids=rubric_ids, storechain_ids=storechain_ids)


def then_response_should_at_least_contain_pois_where(name=None, way=None, postal_codes=None, town_code=None, town_name=None, rubric_ids=None, storechain_ids=None):
    response_should_contain_pois_where(only=False, name=name, way=way, postal_codes=postal_codes, town_code=town_code, town_name=town_name, rubric_ids=rubric_ids, storechain_ids=storechain_ids)


def then_response_should_only_contain_landmarks_where(name=None, postal_codes=None, town_name=None, country_code=None, country_name=None):
    response_should_contain_landmarks_where(only=True, name=name, postal_codes=postal_codes, town_name=town_name, country_code=country_code, country_name=country_name)


def then_response_should_at_least_contain_landmarks_where(name=None, postal_codes=None, town_name=None, country_code=None, country_name=None):
    response_should_contain_landmarks_where(only=False, name=name, postal_codes=postal_codes, town_name=town_name, country_code=country_code, country_name=country_name)


def then_response_should_only_contain_addresses_where(name=None, way_number=None, way=None, postal_codes=None, town_name=None, country_code=None, country_name=None):
    response_should_contain_addresses_where(only=True, name=name, way_number=way_number, way=way, postal_codes=postal_codes, town_name=town_name, country_code=country_code, country_name=country_name)


def then_response_should_at_least_contain_addresses_where(name=None, way_number=None, way=None, postal_codes=None, town_name=None, country_code=None, country_name=None):
    response_should_contain_addresses_where(only=False, name=name, way_number=way_number, way=way, postal_codes=postal_codes, town_name=town_name, country_code=country_code, country_name=country_name)


def then_response_should_only_contain_addresses_and_pois_where(way_number=None, way=None, postal_codes=None, town_name=None, country_name=None):
    response_should_contain_addresses_and_pois_where(only=True, way_number=way_number, way=way, postal_codes=postal_codes, town_name=town_name, country_name=country_name)


def then_response_should_at_least_contain_addresses_and_pois_where(way_number=None, way=None, postal_codes=None, town_name=None, country_name=None):
    response_should_contain_addresses_and_pois_where(only=False, way_number=way_number, way=way, postal_codes=postal_codes, town_name=town_name, country_name=country_name)


def then_response_should_be_inside(bbox):

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")

    if 'addresses' in response:
        for element in response['addresses']['features']:

            address = Address(element)

            if not address.is_in_bbox(bbox):
                assert False, u"Wrong geolocation in '{}'".format(address.name)

    if 'pois' in response:
        for element in response['pois']:

            poi = Poi(element)

            if not poi.is_in_bbox(bbox):
                assert False, u"Wrong geolocation in '{}'".format(poi.name)


def then_response_should_be_outside(bbox):

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")

    if 'addresses' in response:
        for element in response['addresses']['features']:

            address = Address(element)

            if address.is_in_bbox(bbox):
                assert False, u"Wrong geolocation in '{}'".format(address.name)

    if 'pois' in response:
        for element in response['pois']:

            poi = Poi(element)

            if poi.is_in_bbox(bbox):
                assert False, u"Wrong geolocation in '{}'".format(poi.name)


def then_response_should_be_empty():

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")

    if response:
        assert False
    else:
        assert True


def then_response_code_should_be(code):

    # Get response code from global testsuite variables
    response_code = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_CODE}")

    if int(response_code) != int(code):
        assert False
    else:
        assert True


def then_response_should_contain(maximum_results):

    # Get response from global testsuite variables
    response = BuiltIn().run_keyword("Get Variable Value", "${RESPONSE_BODY}")

    pois_number = 0
    addresses_number = 0

    if 'addresses' in response:
        addresses_number = len(response['addresses']['features'])

    if 'pois' in response:
        pois_number = len(response['pois'])

    if (pois_number + addresses_number) > maximum_results:
        assert False
    else:
        assert True
