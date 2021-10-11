from datetime import datetime

from hun_date_parser.date_parser.interval_restriction import extract_within_interval


def test_extract_within_interval():
    tfs = [
        ({'start_date': datetime(2021, 10, 11), 'end_date': datetime(2021, 10, 18, 23, 59, 59)},
         'kedden',
         [{'start_date': datetime(2021, 10, 12), 'end_date': datetime(2021, 10, 12, 23, 59, 59)}]),

        ({'start_date': datetime(2022, 1, 1), 'end_date': datetime(2022, 12, 31, 23, 59, 59)},
         'februárban',
         [{'start_date': datetime(2022, 2, 1), 'end_date': datetime(2022, 2, 28, 23, 59, 59)}]),

        ({'start_date': datetime(2020, 1, 1), 'end_date': datetime(2020, 12, 31, 23, 59, 59)},
         'februárban',
         [{'start_date': datetime(2020, 2, 1), 'end_date': datetime(2020, 2, 29, 23, 59, 59)}]),
    ]

    for interval_restriction, query_sentence, expected in tfs:
        result = extract_within_interval(interval_restriction['start_date'],
                                         interval_restriction['end_date'],
                                         query_sentence)

        assert result == expected
