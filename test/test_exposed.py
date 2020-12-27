from datetime import datetime, date, time

from hun_date_parser import datetime2text, text2datetime, text2date, text2time


def test_datetime2text():
    candidates = datetime2text(datetime(2020, 12, 21))

    assert set(candidates) == {'dates', 'times'}
    assert len([c for c in candidates['dates'] if c]) == 2
    assert len([c for c in candidates['times'] if c]) == 4


def test_text2datetime():
    now = datetime(2020, 12, 27)
    tf = [('ma', [{'start_date': datetime(2020, 12, 27), 'end_date': datetime(2020, 12, 27, 23, 59, 59)}]),
          ('ma reggel', [{'start_date': datetime(2020, 12, 27, 6), 'end_date': datetime(2020, 12, 27, 9, 59, 59)}])]

    for inp, out in tf:
        assert text2datetime(inp, now=now) == out


def test_text2date():
    now = datetime(2020, 12, 27)
    tf = [('ma', [{'start_date': date(2020, 12, 27), 'end_date': date(2020, 12, 27)}]),
          ('ma reggel', [{'start_date': date(2020, 12, 27), 'end_date': date(2020, 12, 27)}]),
          ('reggel nyolc óra', [])]

    for inp, out in tf:
        assert text2date(inp, now=now) == out


def test_text2time():
    now = datetime(2020, 12, 27)
    tf = [('ma', []),
          ('ma reggel', [{'start_date': time(6), 'end_date': time(9, 59, 59)}]),
          ('reggel nyolc óra', [{'start_date': time(8), 'end_date': time(8, 59, 59)}])]

    for inp, out in tf:
        assert text2time(inp, now=now) == out
