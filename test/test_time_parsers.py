import pytest
from datetime import datetime

from hun_date_parser.utils import Year, Month, Day, Daypart, Hour, Minute
from hun_date_parser.date_parser.time_parsers import match_digi_clock, match_time_words, match_now, match_hwords


def test_match_digi_clock():
    fn = 'digi_clock'
    tf = [('kedden 8:45', [[Hour(8, fn), Minute(45, fn)]]),
          ('kedden 08:45', [[Hour(8, fn), Minute(45, fn)]]),
          ('ma este 18:12-kor', [[Hour(18, fn), Minute(12, fn)]])]

    for inp, exp in tf:
        out = match_digi_clock(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


time_word_fn = 'time_words'
time_word_scenarios = [
    ('reggel nyolc előtt hat perccel', [[Hour(7, time_word_fn), Minute(54, time_word_fn)]]),
    ('reggel nyolc előtt nyolcvan perccel', [[Hour(6, time_word_fn), Minute(40, time_word_fn)]]),
    ('este 8 előtt 12 perccel', [[Hour(19, time_word_fn), Minute(48, time_word_fn)]]),
    ('nyolc óra nyolc perckor', [[Hour(8, time_word_fn), Minute(8, time_word_fn)]]),
    ('ma reggel hat óra', [[Hour(6, time_word_fn)]]),
    ('ma reggel', [[Daypart(1, time_word_fn)]]),
    ('ma délután háromkor', [[Hour(15, time_word_fn)]]),
    ('ma délután három után negyvenhat perckor', [[Hour(15, time_word_fn), Minute(46, time_word_fn)]]),
    ('ma délután haemdknc után negyvenhat perckor', [[Daypart(3, time_word_fn)]]),
    ('ma', []),
    ('ötvenöt perckor', []),
    ('húsz óra negyvenkilenc perckor', [[Hour(20, time_word_fn), Minute(49, time_word_fn)]]),
    ('20 óra negyvenkilenc perckor', [[Hour(20, time_word_fn), Minute(49, time_word_fn)]]),
    ('20 óra 49 perckor', [[Hour(20, time_word_fn), Minute(49, time_word_fn)]]),
    ('este 8-kor', [[Hour(20, time_word_fn)]]),
    ('este háromnegyed 8-kor', [[Hour(19, time_word_fn), Minute(45, time_word_fn)]]),
    ('este negyed 8-kor', [[Hour(19, time_word_fn), Minute(15, time_word_fn)]]),
    ('háromnegyed nyolckor', [[Hour(7, time_word_fn), Minute(45, time_word_fn)]]),
    ('este negyed 8 előtt 6 perccel', [[Hour(19, time_word_fn), Minute(9, time_word_fn)]]),
    ('este háromnegyed 8 előtt két perccel', [[Hour(19, time_word_fn), Minute(43, time_word_fn)]]),
    ('este fél 8 előtt harminckilenc perccel', [[Hour(18, time_word_fn), Minute(51, time_word_fn)]]),
    ('este fél 8 előtt', [[Hour(19, time_word_fn), Minute(30, time_word_fn)]]),
    ('harminckilenc perccel este fél 8 előtt', [[Hour(18, time_word_fn), Minute(51, time_word_fn)]]),
    ('mondjuk két perccel 6 után', [[Hour(18, time_word_fn), Minute(2, time_word_fn)]]),
    ('mondjuk tíz perccel 8 óra előtt', [[Hour(7, time_word_fn), Minute(50, time_word_fn)]]),
    ('délután fél négy után hat perccel', [[Hour(15, time_word_fn), Minute(36, time_word_fn)]]),
    ('6 óra után 3 perccel', [[Hour(18, time_word_fn), Minute(3, time_word_fn)]]),
    ('ezen a héten', []),
    ('2020 december', []),
    ('kb húsz év múlva', []),
    ('kb húsz évvel ezelőtt', [])
]


@pytest.mark.parametrize("inp, exp", time_word_scenarios)
def test_match_time_words(inp, exp):
    out = match_time_words(inp)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


def test_match_now():
    now = datetime(2020, 12, 30, 12, 1)
    fn = 'now'
    tf = [('kedden 8:45', []),
          ('most kedden', []),
          ('legyen most',
           [[Year(now.year, fn), Month(now.month, fn), Day(now.day, fn), Hour(now.hour, fn), Minute(now.minute, fn)]])]

    for inp, exp in tf:
        out = match_now(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


hword_fn = 'hwords'
hword_scenarios = [
    ('16h', [[Hour(16, hword_fn)]]),
    ('16 h', []),
    ('16h-kor', [[Hour(16, hword_fn)]]),
    ('h', []),
    ('1 hely', []),
    ('jövő csütörtökön 16h', [[Hour(16, hword_fn)]])
]


@pytest.mark.parametrize("inp, exp", hword_scenarios)
def test_match_hwords(inp, exp):
    out = match_hwords(inp)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp
