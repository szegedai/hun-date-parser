"""This module handles turning datetime instances into Hungarian text."""

from datetime import datetime
from typing import Dict

from hun_date_parser.date_textualizer.date2text import date2text, date2full_text
from hun_date_parser.date_textualizer.time2text import time2absolutetexttime, time2digi, time2relitivetexttime, \
    time2lifelike


def datetime2text(input_datetime: datetime, time_precision: int = 3, now: datetime = datetime.now()):
    """
    Returns date and time textual representation candidates for input datetime object.
    :param input_datetime: Input datetime object.
    :param time_precision: Display only hours, minutes, seconds (corresponding to 1, 2, 3)
    :param now: Current timestamp to calculate relative dates.
    :return: Dictionary with the results
    """
    datetime_textualizer = DatetimeTextualizer(now=now)
    return datetime_textualizer.generate_candidates(input_datetime=input_datetime, time_precision=time_precision)


class DatetimeTextualizer:
    """
    This class handles turning datetime instances into Hungarian text.
    """

    def __init__(self, now: datetime = datetime.now()):
        """
        :param now: Current timestamp to calculate relative dates.
        """
        self.now = now

    def generate_candidates(self, input_datetime: datetime, time_precision: int = 3) -> Dict:
        """
        Generates date and time textual representation candidates for input datetime object.
        :param input_datetime: Input datetime object.
        :param time_precision: Display only hours, minutes, seconds (corresponding to 1, 2, 3)
        :return: Dictionary with the results
        """
        dates = [date2text(input_datetime.date(), self.now.date()),
                 date2full_text(input_datetime.date())]
        times = [time2absolutetexttime(input_datetime.time(), time_precision),
                 time2digi(input_datetime.time(), time_precision),
                 time2relitivetexttime(input_datetime.time(), time_precision),
                 time2lifelike(input_datetime.time())]

        return {
            "dates": dates,
            "times": times
        }
