"""This module handles combined date and time parsing."""

from datetime import datetime, timedelta, date, time
from calendar import monthrange
from itertools import chain

from typing import Dict, List, Union, Tuple
from copy import copy

from hun_date_parser.date_parser.structure_parsers import match_multi_match, match_interval
from hun_date_parser.date_parser.date_parsers import (match_named_month, match_iso_date, match_weekday,
                                                      match_relative_day,
                                                      match_week, match_named_year, match_n_periods_compared_to_now)
from hun_date_parser.date_parser.time_parsers import match_digi_clock, match_time_words, match_now, match_hwords
from hun_date_parser.utils import Year, Month, Week, Day, Daypart, Hour, Minute, monday_of_calenderweek

datelike = Union[datetime, date, time, None]

daypart_mapping = [
    (3, 5),
    (6, 9),
    (10, 11),
    (12, 17),
    (18, 21),
    (22, 2)
]


def text2datetime(input_sentence: str, now: datetime = datetime.now(),
                  expect_future_day: bool = False) -> List[Dict[str, datelike]]:
    """
    Returns the list of datetime intervals found in the input sentence.
    :param input_sentence: Input sentence string.
    :param now: Current timestamp to calculate relative dates.
    :param expect_future_day: Shows if the extracted date will be offset.
    :return: list of datetime interval dictionaries
    """
    datetime_extractor = DatetimeExtractor(now=now, output_container='datetime', expect_future_day=expect_future_day)
    return datetime_extractor.parse_datetime(sentence=input_sentence)


def text2date(input_sentence: str, now: datetime = datetime.now(),
              expect_future_day: bool = False) -> List[Dict[str, datelike]]:
    """
    Returns the list of date intervals found in the input sentence.
    :param input_sentence: Input sentence string.
    :param now: Current timestamp to calculate relative dates.
    :param expect_future_day: Shows if the extracted date will be offset.
    :return: list of date interval dictionaries
    """
    datetime_extractor = DatetimeExtractor(now=now, output_container='date', expect_future_day=expect_future_day)
    return datetime_extractor.parse_datetime(sentence=input_sentence)


def text2time(input_sentence: str, now: datetime = datetime.now(),
              expect_future_day: bool = False) -> List[Dict[str, datelike]]:
    """
    Returns the list of time intervals found in the input sentence.
    :param input_sentence: Input sentence string.
    :param now: Current timestamp to calculate relative dates.
    :param expect_future_day: Shows if the extracted date will be offset.
    :return: list of time interval dictionaries
    """
    datetime_extractor = DatetimeExtractor(now=now, output_container='time', expect_future_day=expect_future_day)
    return datetime_extractor.parse_datetime(sentence=input_sentence)


def match_rules(now: datetime, sentence: str, expect_future_day: bool = False) -> List:
    """
    Matches all rules against input text.
    :param now: Current timestamp to calculate relative dates.
    :param sentence: Input sentence.
    :param expect_future_day: Shows if the extracted date will be offset.
    :return: Parsed date and time classes.
    """
    matches = [*match_named_month(sentence, now),
               *match_iso_date(sentence),
               *match_relative_day(sentence, now),
               *match_weekday(sentence, now, expect_future_day),
               *match_week(sentence, now),
               *match_named_year(sentence, now),
               *match_digi_clock(sentence),
               *match_hwords(sentence),
               *match_time_words(sentence),
               *match_now(sentence, now),
               *match_n_periods_compared_to_now(sentence, now)]

    matches = list(chain(*[m['date_parts'] for m in matches]))

    return matches


def extend_start_end(interval: Dict) -> Dict:
    """
    Heuristic to add missing date and time classes in case of interval.
    :param interval: Dictionary with start and end dateparts.
    :return: Extended dictionary with start and end dateparts.
    """
    if interval['start_date'] == 'OPEN' or interval['end_date'] == 'OPEN':
        return interval

    interval_ = copy(interval)
    for dp in interval['start_date']:
        if type(dp) not in [type(d) for d in interval['end_date']]:
            interval_['end_date'].append(dp)

    return interval_


def type_isin_list(date_type: type, lst: Union[List, str]) -> bool:
    if type(lst) == str:
        return False

    matches = [pot_dp for pot_dp in lst if isinstance(pot_dp, date_type)]

    return bool(matches)


class DatetimeExtractor:
    """
    This class handles combined date and time parsing.
    """

    def __init__(self, now: datetime = datetime.now(), output_container: str = 'datetime',
                 expect_future_day: bool = False) -> None:
        """
        :param now: Current timestamp to calculate relative dates.
        :param output_container: datetime object to populate with datetime parts
        :param expect_future_day: Shows if the extracted date will be offset.
        """
        self.now = now
        self.output_container = output_container
        self.expect_future_day = expect_future_day

    def _get_implicit_intervall(self, sentence_part: str):
        matches = match_rules(self.now, sentence_part, self.expect_future_day)
        return [{'start_date': matches, 'end_date': matches}]

    def assamble_datetime(self, now: datetime,
                          dateparts: Union[List[Union[Year, Month, Week, Day, Daypart, Hour, Minute]], str],
                          bottom: bool = True) -> datelike:
        """
        Assambles parsed date and time classes into datetime instance.
        :param now: Current timestamp to calculate relative dates.
        :param dateparts: List of date and time classes.
        :param bottom: True if the bottom of the interval should be returned, False otherwise
        :param output_container: datetime object to populate with datetime parts
        :return: datetime instance
        """
        res_dt: List[int] = []

        if dateparts == 'OPEN':
            return None
        if not dateparts:
            return None

        has_date, has_time = False, False

        pre_first = True
        for date_type in [Year, Month, Week, Day, Daypart, Hour, Minute]:
            dp_match = [pot_dp for pot_dp in dateparts if isinstance(pot_dp, date_type)]

            _dp_match: Union[Tuple[int, str], None]
            if dp_match:
                _dp_match = dp_match[0]
            else:
                _dp_match = None

            if date_type == Year:
                if _dp_match:
                    has_date = True
                    pre_first = False
                    res_dt.append(_dp_match[0])
                else:
                    # TODO: this should take into account the expect_future_day parameter...
                    res_dt.append(now.year)

            if date_type == Month:
                if _dp_match:
                    has_date = True
                    pre_first = False
                    res_dt.append(_dp_match[0])
                elif pre_first:
                    res_dt.append(now.month)
                elif bottom:
                    res_dt.append(1)
                else:
                    res_dt.append(12)

            if date_type == Week and not type_isin_list(Day, dateparts):
                if _dp_match:
                    has_date = True
                    pre_first = False
                    week2dt = monday_of_calenderweek(res_dt[0], _dp_match[0]) + timedelta(days=(0 if bottom else 6))
                    res_dt = [week2dt.year, week2dt.month, week2dt.day]

            if date_type == Day and len(res_dt) == 2:
                if _dp_match:
                    has_date = True
                    pre_first = False
                    res_dt.append(_dp_match[0])
                elif pre_first:
                    res_dt.append(now.day)
                elif bottom:
                    res_dt.append(1)
                else:
                    mr = monthrange(res_dt[0], res_dt[1])
                    res_dt.append(mr[1])

            if date_type == Daypart:
                if _dp_match:
                    has_time = True
                    pre_first = False
                    dp = _dp_match[0]
                    if bottom:
                        res_dt.append(daypart_mapping[dp][0])
                    elif dp == 5:
                        y, m, d = res_dt
                        next_day = datetime(y, m, d) + timedelta(days=1)
                        res_dt = [next_day.year, next_day.month, next_day.day, daypart_mapping[dp][1]]
                    else:
                        res_dt.append(daypart_mapping[dp][1])

            if date_type == Hour and len(res_dt) == 3:
                if _dp_match:
                    has_time = True
                    pre_first = False
                    res_dt.append(_dp_match[0])
                elif pre_first:
                    res_dt.append(now.hour)
                elif bottom:
                    res_dt.append(0)
                elif not bottom:
                    res_dt.append(23)

            if date_type == Minute:
                if _dp_match:
                    has_time = True
                    pre_first = False
                    res_dt.append(_dp_match[0])
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

        y, m, d, h, mi, s = res_dt

        if self.output_container == 'datetime':
            if has_date or has_time:
                return datetime(y, m, d, h, mi, s)
            else:
                return None
        elif self.output_container == 'date':
            if has_date:
                return date(y, m, d)
            else:
                return None
        elif self.output_container == 'time':
            if has_time:
                return time(h, mi, s)
            else:
                return None
        else:
            return None

    def parse_datetime(self, sentence: str) -> List[Dict[str, datelike]]:
        """
        Extracts list of datetime intervals from input sentence.
        :param sentence: Input sentence string.
        :return: list of datetime interval dictionaries
        """
        sentence = sentence.lower()
        sentence_parts = match_multi_match(sentence)
        parsed_dates = []

        for sentence_part in sentence_parts:
            interval = match_interval(sentence_part)

            if interval:
                interval['start_date'] = 'OPEN' if interval['start_date'] == 'OPEN' else match_rules(self.now, interval[
                    'start_date'], self.expect_future_day)
                interval['end_date'] = 'OPEN' if interval['end_date'] == 'OPEN' else match_rules(self.now, interval[
                    'end_date'], self.expect_future_day)
                parsed_dates.append(interval)
            else:
                parsed_dates += self._get_implicit_intervall(sentence_part)

        parsed_dates = [extend_start_end(intv) for intv in parsed_dates]

        parsed_dates = [{'start_date': self.assamble_datetime(self.now, parsed_date['start_date'], bottom=True),
                         'end_date': self.assamble_datetime(self.now, parsed_date['end_date'], bottom=False)}
                        for parsed_date in parsed_dates]

        parsed_dates = [intv for intv in parsed_dates if intv['start_date'] or intv['end_date']]

        return parsed_dates
