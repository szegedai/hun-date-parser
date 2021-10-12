import pytest
from datetime import datetime

from hun_date_parser.date_parser.interval_restriction import extract_datetime_within_interval, ExtractWithinRangeSuccess


scenarios = [
        ({'start_date': datetime(2021, 10, 11), 'end_date': datetime(2021, 10, 18, 23, 59, 59)},
         'kedden',
         (ExtractWithinRangeSuccess.VALID_IN_RANGE,
          [{'start_date': datetime(2021, 10, 12), 'end_date': datetime(2021, 10, 12, 23, 59, 59)}])),

        ({'start_date': datetime(2022, 1, 1), 'end_date': datetime(2022, 12, 31, 23, 59, 59)},
         'februárban',
         (ExtractWithinRangeSuccess.VALID_IN_RANGE,
          [{'start_date': datetime(2022, 2, 1), 'end_date': datetime(2022, 2, 28, 23, 59, 59)}])),

        ({'start_date': datetime(2020, 1, 1), 'end_date': datetime(2020, 12, 31, 23, 59, 59)},
         'februárban',
         (ExtractWithinRangeSuccess.VALID_IN_RANGE,
          [{'start_date': datetime(2020, 2, 1), 'end_date': datetime(2020, 2, 29, 23, 59, 59)}])),

        ({'start_date': datetime(2020, 1, 1), 'end_date': datetime(2020, 12, 31, 23, 59, 59)},
         'jövő februárban',
         (ExtractWithinRangeSuccess.OUT_OF_RANGE_FALLBACK,
          [{'start_date': datetime(2022, 2, 1), 'end_date': datetime(2022, 2, 28, 23, 59, 59)}])),

        ({'start_date': datetime(2021, 1, 1), 'end_date': datetime(2021, 3, 31, 23, 59, 59)},
         'augusztusban',
         (ExtractWithinRangeSuccess.OUT_OF_RANGE_FALLBACK,
          [{'start_date': datetime(2021, 8, 1), 'end_date': datetime(2021, 8, 31, 23, 59, 59)}])),
    ]


@pytest.mark.parametrize("interval_restriction, query_sentence, expected", scenarios)
def test_extract_within_interval(interval_restriction, query_sentence, expected):
    result = extract_datetime_within_interval(interval_restriction['start_date'],
                                              interval_restriction['end_date'],
                                              query_sentence,
                                              fallback_now=datetime(2021, 10, 11))

    assert result == expected
