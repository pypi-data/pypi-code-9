import datetime
import logging
import unittest

from .test_models import YoutubeStats
from domingo.backends.redis_backend import R


logger = logging.getLogger(__name__)


class ProcessingTests(unittest.TestCase):

    # fixtures = [
    #     'apps/processing/test_fixtures/dashboard.json',
    #     'apps/processing/test_fixtures/networks.json',
    #     # 'apps/processing/test_fixtures/platforms.json',
    #     # 'apps/processing/test_fixtures/scores.json',
    #     # 'apps/processing/test_fixtures/matches.json',
    # ]

    def tearDown(self):
        R.flushdb()
        YoutubeStats.store.collection.drop()

    def test_single_model_redis(self):

        data = {
            "days_since_last_video": [-5.2],
            "view_count": [10],
            "video_count": [5],
            "subscriber_count": [15],
            "outlet_token":  "blahblahblah",
            "comment_count": [20],
            "median_view_count": [25.123123871283],
            'metadata': {
                'name': 'dave',
                'description': 'some channel. not really anything special...'
                }
            }

        yts = YoutubeStats(storage_backend='redis', outlet_type=1, **data)
        yts.save()


        loaded = YoutubeStats.get(outlet_token='blahblahblah')

        for k in data.keys():
            if type(getattr(loaded, k)) == dict:
                for key, val in getattr(loaded, k).items():
                    self.assertEquals(val, getattr(yts, k).get(key))
            else:
                self.assertEquals(getattr(loaded, k), getattr(yts, k))
                self.assertEquals(getattr(loaded, k), data.get(k))

    def test_single_model_rethink(self):
        return
        data = {
            "days_since_last_video": [-5.2],
            "view_count": [10],
            "video_count": [5],
            "subscriber_count": [15],
            "outlet_token":  "blahblahblah",
            "comment_count": [20],
            "median_view_count": [25.123123871283],
            'metadata': {
                'name': 'dave',
                'description': 'some channel. not really anything special...'
                }
            }

        yts = YoutubeStats(storage_backend='rethink', outlet_type=1, **data)
        yts.save()

        loaded = YoutubeStats.get(outlet_token='blahblahblah')

        for k in data.keys():
            if type(getattr(loaded, k)) == dict:
                for key, val in getattr(loaded, k).items():
                    self.assertEquals(val, getattr(yts, k).get(key))
            else:
                self.assertEquals(getattr(loaded, k), getattr(yts, k))
                self.assertEquals(getattr(loaded, k), data.get(k))

    def test_single_model_mongo(self):

        # outlet_token = Char()
        # outlet_type = Int()
        # view_count = List()
        # video_count = List()
        # subscriber_count = List()
        # comment_count = List()
        # median_view_count = List()
        # days_since_last_video = List()

        data = {
            "days_since_last_video": [-5.2],
            "view_count": [10],
            "video_count": [5],
            "subscriber_count": [15],
            "outlet_token":  "blahblahblah",
            "comment_count": [20],
            "median_view_count": [25.123123871283],
            'metadata': {
                'name': 'dave',
                'description': 'some channel. not really anything special...'
            },
            'outlet_type': 'youtube'
        }

        yts = YoutubeStats(storage_backend='mongo', **data)

        yts.save()

        loaded = YoutubeStats.get(outlet_token='blahblahblah')

        for k in data.keys():
            if type(getattr(loaded, k)) == dict:
                for key, val in getattr(loaded, k).items():
                    self.assertEquals(val, getattr(yts, k).get(key))
            else:
                self.assertEquals(getattr(loaded, k), getattr(yts, k))
                self.assertEquals(getattr(loaded, k), data.get(k))

    def test_redis_connection(self):

        d = datetime.datetime.now()
        self.assertTrue(R.set('test', d))
        self.assertEquals(R.get('test'), str(d))
