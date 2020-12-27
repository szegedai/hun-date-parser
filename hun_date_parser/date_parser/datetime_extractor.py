from datetime import datetime, timedelta
from calendar import monthrange
from itertools import chain

from typing import Dict, List, Union
from copy import copy

from hun_date_parser.date_parser.structure_parsers import match_multi_match, match_interval
from hun_date_parser.date_parser.date_parsers import (match_named_month, match_iso_date, match_weekday,
                                                      match_relative_day,
                                                      match_week, match_named_year)
from hun_date_parser.date_parser.time_parsers import match_digi_clock, match_time_words
from hun_date_parser.utils import Year, Month, Week, Day, Daypart, Hour, Minute, monday_of_calenderweek

daypart_mapping = [
    (3, 5),
    (6, 9),
    (10, 11),
    (12, 17),
    (18, 21),
    (22, 2)
]


def assamble_datetime(now: datetime, dateparts: Union[List[Union[Year, Month, Week, Day, Daypart, Hour, Minute]], str],
                      bottom: bool = True):
    res_dt = []

    if dateparts == 'OPEN':
        return None
    if not dateparts:
        return None

    pre_first = True
    for date_type in [Year, Month, Week, Day, Daypart, Hour, Minute]:
        dp_match = [pot_dp for pot_dp in dateparts if isinstance(pot_dp, date_type)]

        if date_type == Year:
            if dp_match:
                pre_first = False
                res_dt.append(dp_match[0][0])
            else:
                res_dt.append(now.year)

        if date_type == Month:
            if dp_match:
                pre_first = False
                res_dt.append(dp_match[0][0])
            elif pre_first:
                res_dt.append(now.month)
            elif bottom:
                res_dt.append(1)
            else:
                res_dt.append(12)

        if date_type == Week:
            if dp_match:
                pre_first = False
                week2dt = monday_of_calenderweek(res_dt[0], dp_match[0][0]) + timedelta(days=(0 if bottom else 6))
                res_dt = [week2dt.year, week2dt.month, week2dt.day]

        if date_type == Day and len(res_dt) == 2:
            if dp_match:
                pre_first = False
                res_dt.append(dp_match[0][0])
            elif pre_first:
                res_dt.append(now.day)
            elif bottom:
                res_dt.append(1)
            else:
                mr = monthrange(res_dt[0], res_dt[1])
                res_dt.append(mr[1])

        if date_type == Daypart:
            if dp_match:
                pre_first = False
                dp = dp_match[0][0]
                if bottom:
                    res_dt.append(daypart_mapping[dp][0])
                elif dp == 5:
                    y, m, d = res_dt
                    next_day = datetime(y, m, d) + timedelta(days=1)
                    res_dt = [next_day.year, next_day.month, next_day.day, daypart_mapping[dp][1]]
                else:
                    res_dt.append(daypart_mapping[dp][1])

        if date_type == Hour and len(res_dt) == 3:
            if dp_match:
                pre_first = False
                res_dt.append(dp_match[0][0])
            elif pre_first:
                res_dt.append(now.hour)
            elif bottom:
                res_dt.append(0)
            elif not bottom:
                res_dt.append(23)

        if date_type == Minute:
            if dp_match:
                pre_first = False
                res_dt.append(dp_match[0][0])
            elif pre_first:
                res_dt.append(now.minute)
            elif bottom:
                res_dt.append(0)
            elif not bottom:
                res_dt.append(59)

    if bottom:
        res_dt.append(0)
    else:
        res_dt.append(59)

    y, m, d, h, mi, se = res_dt
    return datetime(y, m, d, h, mi, se)


def match_rules(now: datetime, sentence: str):
    matches = [*match_named_month(sentence, now),
               *match_iso_date(sentence),
               *match_relative_day(sentence, now),
               *match_weekday(sentence, now),
               *match_week(sentence, now),
               *match_named_year(sentence, now),
               *match_digi_clock(sentence),
               *match_time_words(sentence)]

    matches = list(chain(*[m['date_parts'] for m in matches]))

    return matches


def extend_start_end(interval: Dict):
    if interval['start_date'] == 'OPEN' or interval['end_date'] == 'OPEN':
        return interval

    interval_ = copy(interval)
    for dp in interval['start_date']:
        if type(dp) not in [type(d) for d in interval['end_date']]:
            interval_['end_date'].append(dp)

    return interval_


class DatetimeExtractor:

    def __init__(self, now: datetime = datetime.now()):
        self.now = now

    def _get_implicit_intervall(self, sentence_part: str):
        matches = match_rules(self.now, sentence_part)

        return [{'start_date': matches, 'end_date': matches}]

    def parse_datetime(self, sentence: str):
        sentence_parts = match_multi_match(sentence)
        parsed_dates = []

        for sentence_part in sentence_parts:
            interval = match_interval(sentence_part)

            if interval:
                interval['start_date'] = 'OPEN' if interval['start_date'] == 'OPEN' else match_rules(self.now, interval[
                    'start_date'])
                interval['end_date'] = 'OPEN' if interval['end_date'] == 'OPEN' else match_rules(self.now,
                                                                                                 interval['end_date'])
                parsed_dates.append(interval)
            else:
                parsed_dates += self._get_implicit_intervall(sentence_part)

        parsed_dates = [extend_start_end(intv) for intv in parsed_dates]

        parsed_dates = [{'start_date': assamble_datetime(self.now, parsed_date['start_date'], bottom=True),
                         'end_date': assamble_datetime(self.now, parsed_date['end_date'], bottom=False)}
                        for parsed_date in parsed_dates]

        return parsed_dates
