# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from datetime import date
from datetime import timedelta

from pytz import timezone

from date_calculation import next_draw_date


class DateCalculationTest(unittest.TestCase):
    def setUp(self):
        self.naive_today = datetime.today()
        self.naive_tomorrow = self.naive_today + timedelta(days=1)
        self.tokyo_tz = timezone("Japan")
        self.dublin_tz = timezone("Europe/Dublin")
        self.tokyo_thu_bef = datetime(2018, 5, 31, 03, 58, 00, 207383,
                                      self.tokyo_tz)
        self.tokyo_thu_aft = datetime(2018, 5, 31, 06, 01, 00, 207383,
                                      self.tokyo_tz)
        self.dublin_sun = datetime(2018, 6, 3, 20, 00, 00, 207383,
                                   self.dublin_tz)
        self.dublin_wed_aft = datetime(2018, 5, 31, 20, 47, 00, 207383,
                                       self.dublin_tz)

    def test_invalid_arg(self):
        self.assertRaises(TypeError, next_draw_date, "foobar")

    def test_tokyo_thursday_before_draw(self):
        draw_date = next_draw_date(self.tokyo_thu_bef)
        self.assertEqual(draw_date, date(2018, 5, 30))

    def test_tokyo_thursday_after_draw(self):
        draw_date = next_draw_date(self.tokyo_thu_aft)
        self.assertEqual(draw_date, date(2018, 6, 2))

    def test_dublin_sunday_date(self):
        draw_date = next_draw_date(self.dublin_sun)
        self.assertEqual(draw_date, date(2018, 6, 6))

    def test_dublin_wednesday_after(self):
        draw_date = next_draw_date(self.dublin_wed_aft)
        self.assertEqual(draw_date, date(2018, 6, 2))

if __name__ == '__main__':
    unittest.main()
