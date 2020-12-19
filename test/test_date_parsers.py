from datetime import datetime

from src.date_parser.date_parsers import Year, Month, Week, Day
from src.date_parser.date_parsers import (match_iso_date, match_named_month, match_relative_day, match_weekday,
                                          match_week)


def test_match_iso_date():
    tf = [('2020-01-15', [[Year(2020), Month(1), Day(15)]]),
          ('legyen 2020-01 elején', [[Year(2020), Month(1)]]),
          ('2001-ben történt', [[Year(2001)]]),
          ('2020-12-30-án', [[Year(2020), Month(12), Day(30)]]),
          ('2020-12-30-án 2020.12.29', [[Year(2020), Month(12), Day(30)], [Year(2020), Month(12), Day(29)]])]

    for inp, exp in tf:
        out = match_iso_date(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_named_month():
    now = datetime(2020, 10, 1)

    tf = [('jan 20-án', [[Month(1), Day(20)]]),
          ('2020 febr. 4', [[Month(2), Day(4)]]),
          ('január', [[Month(1)]]),
          (' február ', [[Month(2)]]),
          ('janos', []),
          ('', []),
          ('2020 július', [[Month(7)]]),
          ('2020 június - augusztus 30', [[Month(6)], [Month(8), Day(30)]]),
          ('június 20 - július 30', [[Month(6), Day(20)], [Month(7), Day(30)]]),
          ('tavaly február ', [[Year(2019), Month(2)]]),
          ('legyen jövő február 12-én', [[Year(2021), Month(2), Day(12)]]),
          ('legyen jövő év február 12-én', [[Year(2021), Month(2), Day(12)]]),
          ('legyen jövőre február 12-én', [[Year(2021), Month(2), Day(12)]])]

    for inp, exp in tf:
        out = match_named_month(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_relative_day():
    now = datetime(2020, 10, 1)

    tf = [('ma', [[Year(2020), Month(10), Day(1)]]),
          ('ma-holnap', [[Year(2020), Month(10), Day(1)], [Year(2020), Month(10), Day(2)]]),
          ('holnapután reggel nyolc', [[Year(2020), Month(10), Day(3)]]),
          ('legyen ma reggel', [[Year(2020), Month(10), Day(1)]]),
          ('miért nem jöttél tegnap? na majd ma', [[Year(2020), Month(10), Day(1)], [Year(2020), Month(9), Day(30)]])]

    for inp, exp in tf:
        out = match_relative_day(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_relative_day():
    now = datetime(2020, 12, 7) # monday

    tf = [('múlt vasárnap', [[Year(2020), Month(12), Day(6)]]),
          ('ezen a heten hetfon', [[Year(2020), Month(12), Day(7)]]),
          ('jövő kedden', [[Year(2020), Month(12), Day(15)]]),
          ('előző szombaton ', [[Year(2020), Month(12), Day(5)]]),
          ('miért nem jöttél tegnap? na majd ma', [])]

    for inp, exp in tf:
        out = match_weekday(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_relative_week():
    now = datetime(2020, 12, 7)

    tf = [('múlthéten', [[Year(2020), Week(49)]]),
          ('múlt hét kedden', [[Year(2020), Week(49)]]),
          ('ezen a heten hetfon', [[Year(2020), Week(50)]]),
          ('jövőhéten', [[Year(2020), Week(51)]]),
          ('legyen ma', [])]

    for inp, exp in tf:
        out = match_week(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp
