from datetime import datetime

from src.date_parser.utils import Year, Month, Week, Day, Hour, Minute, Second
from src.date_parser.time_parsers import match_digi_clock


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
