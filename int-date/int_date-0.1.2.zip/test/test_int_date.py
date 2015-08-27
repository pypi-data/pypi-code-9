from unittest import TestCase
import datetime
from hamcrest import assert_that, equal_to, greater_than
import int_date

__author__ = 'Cedric Zhuang'


class TestIntDate(TestCase):
    def test_get_date_from_int(self):
        date = int_date.get_date_from_int(20120515)
        assert_that(date.year, equal_to(2012))
        assert_that(date.month, equal_to(5))
        assert_that(date.day, equal_to(15))

    def test_get_date_from_int_error(self):
        with self.assertRaises(ValueError):
            int_date.get_date_from_int(20120532)

    def test_get_day_interval(self):
        interval = int_date.get_int_day_interval(20120530, 20120602)
        assert_that(interval, equal_to(3))

    def test_get_day_interval_negative(self):
        interval = int_date.get_int_day_interval(20120503, 20120324)
        assert_that(interval, equal_to(-40))

    def test_get_date_from_diff_before(self):
        assert_that(int_date.get_date_from_diff(20120503, -40),
                    equal_to(20120324))

    def test_get_date_from_diff_zero(self):
        assert_that(int_date.get_date_from_diff(20120503, 0),
                    equal_to(20120503))

    def test_get_date_from_diff_next(self):
        assert_that(int_date.get_date_from_diff(20120228, 2),
                    equal_to(20120301))

    def test_to_int_date(self):
        date = int_date.to_int_date(datetime.datetime(2015, 5, 21))
        assert_that(date, equal_to(20150521))

    def test_to_int_date_str_1(self):
        date = int_date.to_int_date('2015-1-3')
        assert_that(date, equal_to(20150103))

    def test_to_int_date_str_2(self):
        date = int_date.to_int_date('2015/11/23')
        assert_that(date, equal_to(20151123))

    def test_to_int_date_unicode(self):
        date = int_date.to_int_date(u'2015/11/23')
        assert_that(date, equal_to(20151123))

    def test_to_int_date_str_error(self):
        with self.assertRaises(ValueError):
            int_date.to_int_date('20151301')

    def test_date_to_int_none(self):
        with self.assertRaises(ValueError):
            int_date.to_int_date(None)

    def test_in_month(self):
        assert_that(int_date.in_month(20140503, [3, 5, 7]), equal_to(True))
        assert_that(int_date.in_month(20140503, {3, 5, 7}), equal_to(True))
        assert_that(int_date.in_month(20140503, (3, 5, 7)), equal_to(True))
        assert_that(int_date.in_month(20140131, [3, 5, 7]), equal_to(False))
        assert_that(int_date.in_month(20140131, 1), equal_to(True))
        assert_that(int_date.in_month(20140131, 3), equal_to(False))

    def test_in_date(self):
        assert_that(int_date.in_date(20140503, [3, 5, 7]), equal_to(True))
        assert_that(int_date.in_date(20140503, {1, 5, 7}), equal_to(False))
        assert_that(int_date.in_date(20140131, 31), equal_to(True))
        assert_that(int_date.in_date(20140131, 30), equal_to(False))

    def test_in_year(self):
        assert_that(int_date.in_year(20140503, [2013, 2014]), equal_to(True))
        assert_that(int_date.in_year(20140503, {2013, 2015}), equal_to(False))
        assert_that(int_date.in_year(20140131, 2014), equal_to(True))
        assert_that(int_date.in_year(20140131, 2013), equal_to(False))

    def test_today(self):
        today = int_date.today()
        assert_that(today, greater_than(20150504))
