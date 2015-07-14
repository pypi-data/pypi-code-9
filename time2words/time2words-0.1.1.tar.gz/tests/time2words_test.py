import unittest

import time2words


class _TestAproxTime(unittest.TestCase):

    def test_less_than_1m(self):
        self.assertEqual(
            time2words.relative_time_to_text(seconds=30), "thirty seconds")

        self.assertEqual(
            time2words.relative_time_to_text(seconds=24),
            "twenty-four seconds")

        self.assertEqual(
            time2words.relative_time_to_text(seconds=1), "one second")

        self.assertEqual(
            time2words.relative_time_to_text(seconds=11), "eleven seconds")

    def test_between_1m_and_1h(self):
        self.assertEqual(
            time2words.relative_time_to_text(minutes=1, seconds=30),
            "about one minute")

        self.assertEqual(
            time2words.relative_time_to_text(minutes=36, seconds=45),
            "about thirty-six minutes")

    def test_between_1h_and_23h(self):
        self.assertEqual(
            time2words.relative_time_to_text(hours=6, minutes=34),
            "six and a half hours")

        self.assertEqual(
            time2words.relative_time_to_text(hours=3, minutes=15),
            "more than three hours")

        self.assertEqual(
            time2words.relative_time_to_text(hours=7, minutes=54),
            "less than eight hours")

        self.assertEqual(
            time2words.relative_time_to_text(hours=13, minutes=57),
            "about fourteen hours")

    def test_between_23h_and_6d1h(self):
        self.assertEqual(
            time2words.relative_time_to_text(hours=23, minutes=30),
            "one day")

        self.assertEqual(
            time2words.relative_time_to_text(days=2, hours=13),
            "about two and a half days"
        )

        self.assertEqual(
            time2words.relative_time_to_text(days=4, hours=17),
            "a little less than five days"
        )

    def test_between_6d1h_and_25d10h(self):
        self.assertEqual(
            time2words.relative_time_to_text(days=11, hours=13),
            "about one and a half week"
        )

        self.assertEqual(
            time2words.relative_time_to_text(days=22, hours=11),
            "about three weeks"
        )

    def test_between_25d10h_and_11mm(self):
        self.assertEqual(
            time2words.relative_time_to_text(months=6, weeks=3, days=5),
            "about seven months"
        )

        self.assertEqual(
            time2words.relative_time_to_text(months=9, weeks=2),
            "about nine and a half months"
        )

    def test_between_11mm_and_11y(self):
        self.assertEqual(
            time2words.relative_time_to_text(months=11, days=5),
            "about one year"
        )

        self.assertEqual(
            time2words.relative_time_to_text(years=5, months=8, days=5),
            "less than six years"
        )

        self.assertEqual(
            time2words.relative_time_to_text(years=4, months=5),
            "about four and a half years"
        )

    def test_more_than_11y(self):
        self.assertEqual(
            time2words.relative_time_to_text(years=50, months=3),
            "about fifty years"
        )


if __name__ == '__main__':
    unittest.main()
