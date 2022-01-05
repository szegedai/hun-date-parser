"""
This module (still WIP) implements extracting datetime intervals from pre-determined datetime intervals.
If extraction within the set interval is not successful, the extraction falls back to the text2datetime function
"""

from datetime import datetime, date, time, timedelta
from enum import Enum
from typing import Dict, List, Union, Tuple
from copy import deepcopy

from hun_date_parser import text2datetime
from hun_date_parser.utils import remove_accent
from hun_date_parser.date_parser.time_parsers import _raw_match_time_words

datelike = Union[datetime, date, time, None]


def get_reversed_am_pm(dt: datetime):
    dt_ = deepcopy(dt)
    if 0 < dt.hour < 12:
        dt_ = datetime(dt.year, dt.month, dt.day, dt.hour + 12, dt.minute, dt.second)
    elif not (dt.hour == 23 and dt.minute == 59) and dt.hour > 12:
        dt_ = datetime(dt.year, dt.month, dt.day, dt.hour - 12, dt.minute, dt.second)
    elif dt.hour == 12:
        dt_ = dt_ + timedelta(days=1)
        dt_ = datetime(dt_.year, dt_.month, dt_.day, 0, dt_.minute, dt_.second)

    return dt_


class ExtractWithinRangeSuccess(Enum):
    VALID_IN_RANGE = 'in_range'
    OUT_OF_RANGE_FALLBACK = 'out_of_range'
    RELATIVE_TIME_WORD_FALLBACK = 'relative_time_word'
    OPEN_RANGE_FALLBACK = 'open_range'
    NO_MATCH_FALLBACK = 'no_match'


def is_relative_datetime(query: str):
    """
    Determines wheter the query text refers to a relative datetime, ie.: next monday
    """
    relative_time_words = ['ma', 'holnap', 'holnaput', 'tegnap', 'tegnapel', 'jovo', 'mult']
    transformed_query = remove_accent(query)

    for time_word in relative_time_words:
        if time_word in transformed_query:
            return True

    return False


def extract_datetime_within_interval(interval_start: datetime,
                                     interval_end: datetime,
                                     query_text: str,
                                     expect_future_day: bool = False,
                                     fallback_now=datetime.now()) -> Tuple[ExtractWithinRangeSuccess,
                                                                           List[Dict[str, datelike]]]:
    """
    Extracts datetime intervals from pre-determined datetime intervals.
    :param interval_start: Bounding interval start
    :param interval_end: Bounding interval end
    :param query_text: Text to extract datetime interval from
    :param expect_future_day: Shows if the extracted date will be offset.
    :param fallback_now: When interval restriction is unsuccessful (RELATIVE_TIME_WORD_FALLBACK, OUT_OF_RANGE_FALLBACK)
    the text2datetime function's result is returned, which can be supplied with a pseudo-now datetime
    :return: success flag, restricted time interval
    """

    res = text2datetime(query_text,
                        expect_future_day=expect_future_day,
                        now=interval_start)

    possible_am_pm_missmatch = False
    parts = _raw_match_time_words(query_text)
    if parts:
        group, daypart, hour_modifier, hour, minute = parts
        if not daypart and hour:
            possible_am_pm_missmatch = True

    extend_res = []
    if possible_am_pm_missmatch:
        for match in res:
            if isinstance(match["start_date"], datetime) and isinstance(match["end_date"], datetime):
                extend_res.append({
                        "start_date": get_reversed_am_pm(match["start_date"]),
                        "end_date": get_reversed_am_pm(match["end_date"])
                    })

    res += extend_res

    restricted_date: List[Dict[str, datelike]] = []
    response_candidates = [(5, ExtractWithinRangeSuccess.NO_MATCH_FALLBACK, restricted_date)]
    for r in res:
        if not (isinstance(r['start_date'], datetime) and isinstance(r['end_date'], datetime)):
            response_type = ExtractWithinRangeSuccess.OPEN_RANGE_FALLBACK
            restricted_date = text2datetime(query_text,
                                            expect_future_day=expect_future_day,
                                            now=fallback_now)

            response_candidates.append((4, response_type, restricted_date))
            continue

        assert type(interval_start) == datetime and type(r['start_date']) == datetime
        assert type(interval_end) == datetime and type(r['end_date']) == datetime
        if not (interval_start <= r['start_date'] and r['end_date'] <= interval_end):
            # Extracted datetime is out of expected interval...
            response_type = ExtractWithinRangeSuccess.OUT_OF_RANGE_FALLBACK
            restricted_date = text2datetime(query_text,
                                            expect_future_day=expect_future_day,
                                            now=fallback_now)

            response_candidates.append((2, response_type, restricted_date))
            continue

        if is_relative_datetime(query_text):
            # Datetime ranges relative to the current timestamp doesn't really make sense in this scenario...
            response_type = ExtractWithinRangeSuccess.RELATIVE_TIME_WORD_FALLBACK
            restricted_date = text2datetime(query_text,
                                            expect_future_day=expect_future_day,
                                            now=fallback_now)

            response_candidates.append((3, response_type, restricted_date))
        else:
            response_type = ExtractWithinRangeSuccess.VALID_IN_RANGE
            restricted_date = [r]

            response_candidates.append((1, response_type, restricted_date))

    response_candidates_ranked = sorted(response_candidates)
    _, response_type, restricted_date = response_candidates_ranked[0]

    return response_type, restricted_date
