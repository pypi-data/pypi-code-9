from django.test import TestCase
from django.conf import settings
from .models import GmapsPlace, GmapsItem
from gmaps import Geocoding
from gmaps.errors import RateLimitExceeded
import json


class GmapsPlacesTest(TestCase):

    @classmethod
    def setUpClass(cls):
        location1 = GmapsPlace(
            address='Pippo, Brentwood, CA 94513, USA')
        location1.process_address()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_gmaps_items_exists(self):
        self.assertNotEqual(GmapsItem.objects.all().count(), 0)

    def test_gmaps_items_have_place_id(self):
        for gmi in GmapsItem.objects.all():
            self.assertNotIn(gmi.place_id, ["", None])

    def test_json_like_geocode_call(self):
        gmaps_api = Geocoding(
            **{
                'sensor': True,
                'use_https': True,
                'api_key': u'{}'.format(settings.GMAPS_API_KEY)}
        )
        california = GmapsItem.objects.get(short_name="CA")
        california_response = california.get_response_json()
        geocode_response = gmaps_api.geocode(california.geo_address, **{'language': 'en'})
        self.assertEqual(california_response, json.dumps(geocode_response))

    def test_insert_more_places(self):
        location2 = GmapsPlace(
            address='Olympic Stadium, Viale dello Stadio Olimpico, 00135 Roma, Italy')
        location2.process_address()
        print("Stadio Flaminio address is a gmaps api BUG. https://code.google.com/p/gmaps-api-issues/issues/detail?id=8500 . We should check for fixes.")
        location3 = GmapsPlace(
            address='Stadio Flaminio, Piazza Maresciallo Pilsudski, 00196 Roma, Italy')
        location3.process_address()

    def test_massive_gmaps_requests_fail(self):
        gmaps_api = Geocoding(
            **{
                'sensor': True,
                'use_https': True,
                'api_key': u''
            }
        )
        with self.assertRaises(RateLimitExceeded):
            for x in xrange(100):
                gmaps_api.geocode('Pippo, Brentwood, CA 94513, USA', **{'language': 'en'})

    def test_massive_gmaps_requests_ok(self):
        gmi = GmapsItem.objects.last()
        for x in xrange(100):
            gmi.get_response_json()
