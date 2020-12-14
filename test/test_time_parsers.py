from datetime import datetime

from src.date_parser.utils import Year, Month, Week, Day, Daypart, Hour, Minute, Second
from src.date_parser.time_parsers import match_digi_clock, match_time_words


def test_match_relative_week():
    tf = [('kedden 8:45', [[Hour(8), Minute(45)]]),
          ('kedden 08:45', [[Hour(8), Minute(45)]]),
          ('ma este 18:12-kor', [[Hour(18), Minute(12)]])]

    for inp, exp in tf:
        out = match_digi_clock(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_time_words():
    tf = [('reggel nyolc előtt hat perccel', [[Hour(8), Minute(6)]]),  # TODO: add this functionality
          ('nyolc óra nyolc perckor', [[Hour(8), Minute(8)]]),
          ('ma reggel hat óra', [[Hour(6)]]),
          ('ma reggel', [[Daypart(1)]]),
          ('ma délután háromkor', [[Hour(15)]]),
          ('ma délután három után negyvenhat perckor', [[Hour(15), Minute(46)]]),
          ('ma délután haemdknc után negyvenhat perckor', [[Daypart(3)]]),
          ('ma', []),
          ('ötvenöt perckor', []),
          ('húsz óra negyvenkilenc perckor', [[Hour(20), Minute(49)]]),
          ('20 óra negyvenkilenc perckor', [[Hour(20), Minute(49)]]),
          ('20 óra 49 perckor', [[Hour(20), Minute(49)]]),
          ('este 8-kor', [[Hour(20)]])]

    for inp, exp in tf:
        out = match_time_words(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp