from datetime import datetime

from hun_date_parser import datetime2text, text2datetime


def test_datetime2text():
    candidates = datetime2text(datetime(2020, 12, 21))

    assert set(candidates) == {'dates', 'times'}
    assert len([c for c in candidates['dates'] if c]) == 2
    assert len([c for c in candidates['times'] if c]) == 4


def test_text2datetime():
    now = datetime(2020, 12, 27)
    tf = [('ma', [{'start_date': datetime(2020, 12, 27), 'end_date': datetime(2020, 12, 27, 23, 59, 59)}])]

    for inp, out in tf:
        assert text2datetime(inp, now=now) == out
