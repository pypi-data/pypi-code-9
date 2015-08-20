from django.test import TestCase
from django.conf import settings
from .models import GmapsPlace, GmapsItem
from gmaps import Geocoding
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

    def test_insert_second_place(self):
        location2 = GmapsPlace(
            address='Olympic Stadium, Viale dello Stadio Olimpico, 00135 Roma, Italy')
        location2.process_address()
