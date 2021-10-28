"""
This module (still WIP) implements extracting datetime intervals from pre-determined datetime intervals.
If extraction within the set interval is not successful, the extraction falls back to the text2datetime function
"""

from datetime import datetime, date, time
from enum import Enum
from typing import Dict, List, Union, Tuple

from hun_date_parser import text2datetime
from hun_date_parser.utils import remove_accent

datelike = Union[datetime, date, time, None]


class ExtractWithinRangeSuccess(Enum):
    VALID_IN_RANGE = 'in_range'
    OUT_OF_RANGE_FALLBACK = 'out_of_range'
    RELATIVE_TIME_WORD_FALLBACK = 'relative_time_word'
    OPEN_RANGE_FALLBACK = 'open_range'


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

    for r in res:
        if not (type(r['start_date']) == datetime and type(r['start_date']) == datetime):
            return ExtractWithinRangeSuccess.OPEN_RANGE_FALLBACK, text2datetime(query_text,
                                                                                expect_future_day=expect_future_day,
                                                                                now=fallback_now)

        assert type(interval_start) == datetime and type(r['start_date']) == datetime
        assert type(interval_end) == datetime and type(r['end_date']) == datetime
        if not (interval_start <= r['start_date'] and r['end_date'] <= interval_end):
            # Extracted datetime is out of expected interval...
            return ExtractWithinRangeSuccess.OUT_OF_RANGE_FALLBACK, text2datetime(query_text,
                                                                                  expect_future_day=expect_future_day,
                                                                                  now=fallback_now)

    if is_relative_datetime(query_text):
        # Datetime ranges relative to the current timestamp doesn't really make sense in this scenario...
        return ExtractWithinRangeSuccess.RELATIVE_TIME_WORD_FALLBACK, text2datetime(query_text,
                                                                                    expect_future_day=expect_future_day,
                                                                                    now=fallback_now)
    else:
        return ExtractWithinRangeSuccess.VALID_IN_RANGE, res
