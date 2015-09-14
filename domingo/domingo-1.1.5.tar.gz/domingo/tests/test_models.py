import unittest

from domingo import models
from domingo.fields import List, Char, Dict, Int
from domingo.utils import utcnow, utcstamp


class YoutubeStats(models.AsyncModel):
    """
        mostly just used for testing.
    """
    unique_on = ['outlet_token', 'outlet_type']

    outlet_token = Char()
    outlet_type = Char()
    view_count = List()
    video_count = List()
    subscriber_count = List()
    comment_count = List()
    median_view_count = List()
    days_since_last_video = List()

    metadata = Dict()


class ModelBaseTests(unittest.TestCase):

    def setUp(self):
        self.model_instance = models.SimpleModel()
        self.async_instance = models.AsyncModel()
        self.yts_instance = YoutubeStats()

    # @unittest.skip('Skipping for now. Runs strangely sometimes.')
    def test_instantiation_time(self):
        fake_data = dict(
            outlet_token='asdlfkjasldfkj',
            outlet_type=int(),
            view_count=range(2),
            video_count=range(2),
            subscriber_count=range(2),
            comment_count=range(2),
            median_view_count=range(2),
            days_since_last_video=range(2)
        )

        diffs = []
        for i in range(500):
            start = utcstamp()
            YoutubeStats(**fake_data)
            finish = utcstamp()
            diff = finish - start
            diffs.append(diff)
        avg_diff = sum(diffs) / 500.

        limits = [0.01, 0.0025, 0.002, 0.0015, 0.001, 0.00053]
        for limit in limits:
            self.assertLess(
                avg_diff, limit,
                "Instantiation of a model takes too long. Limit was %f secs."
                "Took %f seconds" % (limit, diff)
            )

    def test_namespace(self):
        "Tests that inheritance doesn't effect the namespace"
        self.assertEqual(models.SimpleModel.namespace, 'simplemodel')
        self.assertEqual(self.model_instance.namespace, 'simplemodel')

        self.assertEqual(models.AsyncModel.namespace, 'asyncmodel')
        self.assertEqual(self.async_instance.namespace, 'asyncmodel')

        self.assertEqual(YoutubeStats.namespace, 'youtubestats')
        self.assertEqual(self.yts_instance.namespace, 'youtubestats')

    def test_model_instance_specific_fields(self):
        """
        test that the two (class field and instance field) are not the same
        object
        """
        # it also tests that ModelBase has the Timestamp field added by default
        self.assertFalse(
            self.async_instance.created is models.AsyncModel._meta.created
        )

    def test_model_instance_fields_getattr(self):
        """
        The value of all fields within self._fields should be
        equivalent to the attribute
        named on the instance
        """
        created = self.async_instance._fields['created']
        self.assertTrue(
            created.value is self.async_instance.created
        )

    def test_setattr(self):
        """
        You should be able to set the value of a local field by 'normal' means,
        i.e. model.field = value
        """
        time = utcnow()
        self.async_instance.created = time
        self.assertNotEqual(
            models.AsyncModel._meta.created, self.async_instance.created
        )
        self.assertEqual(self.async_instance.created, time)