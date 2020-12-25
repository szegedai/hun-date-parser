from datetime import datetime

from hun_date_parser.date_textualizer.date2text import date2text, date2full_text
from hun_date_parser.date_textualizer.time2text import time2absolutetexttime, time2digi, time2relitivetexttime, time2lifelike


class DatetimeTextualizer:

    def __init__(self, now: datetime = datetime.now()):
        self.now = now

    def generate_candidates(self, datetime: datetime, time_precision: int = 3):
        dates = [date2text(datetime.date(), self.now.date()),
                 date2full_text(datetime.date())]
        times = [time2absolutetexttime(datetime.time(), time_precision),
                 time2digi(datetime.time(), time_precision),
                 time2relitivetexttime(datetime.time(), time_precision),
                 time2lifelike(datetime.time())]

        return {
            "date": dates,
            "times": times
        }
