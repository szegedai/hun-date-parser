import pytest
from datetime import datetime, date, time

from hun_date_parser import datetime2text, text2datetime, text2date, text2time
from hun_date_parser.utils import SearchScopes


def test_datetime2text():
    candidates = datetime2text(datetime(2020, 12, 21))

    assert set(candidates) == {'dates', 'times'}
    assert len([c for c in candidates['dates'] if c]) == 2
    assert len([c for c in candidates['times'] if c]) == 4


tf_t2d = [
    ('ma', [{'start_date': datetime(2020, 12, 27), 'end_date': datetime(2020, 12, 27, 23, 59, 59)}],
     SearchScopes.NOT_RESTRICTED, True),
    ('ma reggel', [{'start_date': datetime(2020, 12, 27, 6), 'end_date': datetime(2020, 12, 27, 10, 59, 59)}],
     SearchScopes.NOT_RESTRICTED, True),
    ('ma reggeltől tegnap estig', [], SearchScopes.NOT_RESTRICTED, True),
    ('Egerben leszek december 28-ától 2 napig',
     [{'start_date': datetime(2020, 12, 28), 'end_date': datetime(2020, 12, 30, 23, 59, 59)}],
     SearchScopes.NOT_RESTRICTED, True),
    ('8000 forint', [], SearchScopes.NOT_RESTRICTED, True),
    ('8000 forint', [], SearchScopes.PAST_SEARCH, True),
    ('8000', [], SearchScopes.NOT_RESTRICTED, True),
    ('8000', [], SearchScopes.PAST_SEARCH, True),
    ('8000', [{'start_date': datetime(8000, 1, 1), 'end_date': datetime(8000, 12, 31, 23, 59, 59)}],
     SearchScopes.NOT_RESTRICTED, False),
    ('8000', [{'start_date': datetime(8000, 1, 1), 'end_date': datetime(8000, 12, 31, 23, 59, 59)}],
     SearchScopes.PAST_SEARCH, False),
    ('8000', [{'start_date': datetime(8000, 1, 1), 'end_date': datetime(8000, 12, 31, 23, 59, 59)}],
     SearchScopes.FUTURE_DAY, False),
    ('8000 forint', [], SearchScopes.FUTURE_DAY, False),
]


@pytest.mark.parametrize("inp, out, search_scope, realistic_year_restriction", tf_t2d)
def test_text2datetime(inp, out, search_scope, realistic_year_restriction):
    now = datetime(2020, 12, 27)
    assert text2datetime(inp, now=now, search_scope=search_scope,
                         realistic_year_required=realistic_year_restriction) == out


@pytest.mark.parametrize("inp, out, search_scope, realistic_year_restriction", tf_t2d)
def test_text2datetime_default(inp, out, search_scope, realistic_year_restriction):

    if not realistic_year_restriction or search_scope != SearchScopes.NOT_RESTRICTED:
        return

    now = datetime(2020, 12, 27)
    assert text2datetime(inp, now=now) == out


def test_text2date():
    now = datetime(2020, 12, 27)
    tf = [('ma', [{'start_date': date(2020, 12, 27), 'end_date': date(2020, 12, 27)}]),
          ('ma reggel', [{'start_date': date(2020, 12, 27), 'end_date': date(2020, 12, 27)}]),
          ('reggel nyolc óra', []),
          ('8000 Forint', []),
          ("MZ/X kr.u. 3000-ben született", []),
          ("100000 nap múlva", [{'end_date': date(2294, 10, 12), 'start_date': date(2294, 10, 12)}])]

    for inp, out in tf:
        assert text2date(inp, now=now) == out


def test_text2date_no_restriction():
    now = datetime(2020, 12, 27)
    tf = [
        ('8000', [{'start_date': date(8000, 1, 1), 'end_date': date(8000, 12, 31)}]),
        ('8000 forint', []),
        ("MZ/X kr.u. 3000-ben született", [{'start_date': date(3000, 1, 1), 'end_date': date(3000, 12, 31)}])
    ]

    for inp, out in tf:
        assert text2date(inp, now=now, search_scope=SearchScopes.NOT_RESTRICTED, realistic_year_required=False) == out


def test_text2time():
    now = datetime(2020, 12, 27)
    tf = [('ma', []),
          ('ma reggel', [{'start_date': time(6), 'end_date': time(10, 59, 59)}]),
          ('ma délelőtt', [{'start_date': time(8), 'end_date': time(11, 59, 59)}]),
          ('reggel nyolc óra', [{'start_date': time(8), 'end_date': time(8, 59, 59)}])]

    for inp, out in tf:
        assert text2time(inp, now=now) == out
