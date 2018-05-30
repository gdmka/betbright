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
    wednesday_daynum = 2
    saturday_daynum = 5
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

    if current_weekday <= wednesday_daynum:
        if (current_weekday % wednesday_daynum) == 0 and \
           (dublin_dt.hour < draw_hour_start):
            next_draw = dublin_dt.date()
            logging.info("Next draw date {}".format(next_draw))
            return next_draw
        else:
            days_til_wed = 3 if (wednesday_daynum - current_weekday == 0) \
                else wednesday_daynum - current_weekday
            next_draw = (dublin_dt + timedelta(days=days_til_wed)).date()
            logging.info("Next draw date {}".format(next_draw))
            return next_draw

    if current_weekday <= saturday_daynum:
        if (current_weekday % saturday_daynum == 0) and \
           (dublin_dt.hour < draw_hour_start):
            next_draw = dublin_dt.date()
            logging.info("Next draw date {}".format(next_draw))
            return next_draw
        else:
            days_til_sat = 3 if (saturday_daynum - current_weekday == 0) \
                else saturday_daynum - current_weekday
            next_draw = (dublin_dt + timedelta(days=days_til_sat)).date()
            logging.info("Next draw date {}".format(next_draw))
            return next_draw

    if current_weekday == 6:  # handle Sunday case
        next_draw = (dublin_dt + timedelta(days=3)).date()
        logging.info("Next draw date {}".format(next_draw))
        return next_draw
