# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta


import pytz
from tzlocal import get_localzone

from logger import configure_logger

logging = configure_logger(filename="date_calculation.log",
                           logger_name="date_calculation")


def next_draw_date(date_time=None):
    """Calculate next draw date of irish lottery.

        Args:
            dt (:obj: `datetime.datetime`, optional): point in time to find
            next draw date to

        Returns:
            datetime.date object.

        Exception:
            If an exception will occur function will return None.
    """

    if not isinstance(date_time, datetime):
        logging.error("Invalid arg '{}' of {}".format(date_time,
                                                      type(date_time)))
        raise TypeError("Invalid arg '{}' of {}".format(date_time,
                                                        type(date_time)))

    draw_hour_start = 20

    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = xrange(7)

    days_till_wednesday = (SUNDAY, MONDAY, TUESDAY)
    days_after_wednesday = (THURSDAY, FRIDAY)

    next_draw = None

    if date_time is None:
        date_time = datetime.now(get_localzone())

    logging.info("Local DateTime: {}".format(date_time))

    try:
        if date_time.tzinfo is None:  # Handle naive date time case
            date_time = date_time.replace(tzinfo=get_localzone())

        logging.info("Local Timezone Info: {}".format(date_time.tzinfo))

        dublin_tz = pytz.timezone('Europe/Dublin')

        dublin_dt = date_time.astimezone(dublin_tz)
        logging.info("Dublin DateTime: {}".format(dublin_dt))

    except Exception as e:
        logging.error(e.message)
        return

    current_weekday = dublin_dt.weekday()
    logging.info("Current day number: {}".format(current_weekday))

    if current_weekday in days_till_wednesday:
        delta = 3 if current_weekday == SUNDAY else WEDNESDAY - current_weekday
        next_draw = (dublin_dt + timedelta(days=delta)).date()

    if current_weekday in days_after_wednesday:
        next_draw = (dublin_dt + timedelta(days=SATURDAY - current_weekday)).date()

    if current_weekday == WEDNESDAY:
        if dublin_dt.hour < draw_hour_start:
            next_draw = dublin_dt.date()

        else:
            next_draw = (dublin_dt + timedelta(days=SATURDAY - WEDNESDAY)).date()

    if current_weekday == SATURDAY:
        if dublin_dt.hour < draw_hour_start:
            next_draw = dublin_dt.date()

        else:
            next_draw = (dublin_dt + timedelta(days=SATURDAY - current_weekday)).date()

    logging.info("Next draw date {}".format(next_draw))

    return next_draw
