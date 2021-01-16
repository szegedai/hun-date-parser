from datetime import datetime

from hun_date_parser.date_parser.date_parsers import Year, Month, Week, Day
from hun_date_parser.date_parser.date_parsers import (match_iso_date, match_named_month, match_relative_day, match_weekday,
                                                      match_week, match_named_year)


def test_match_iso_date():
    fn = 'match_iso_date'
    tf = [('2020-01-15', [[Year(2020, fn), Month(1, fn), Day(15, fn)]]),
          ('legyen 2020-01 elején', [[Year(2020, fn), Month(1, fn)]]),
          ('2001-ben történt', [[Year(2001, fn)]]),
          ('2020-12-30-án', [[Year(2020, fn), Month(12, fn), Day(30, fn)]]),
          ('2020-12-30-án 2020.12.29',
           [[Year(2020, fn), Month(12, fn), Day(30, fn)], [Year(2020, fn), Month(12, fn), Day(29, fn)]])]

    for inp, exp in tf:
        out = match_iso_date(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_named_month():
    fn = 'named_month'
    now = datetime(2020, 10, 1)

    tf = [('jan 20-án', [[Month(1, fn), Day(20, fn)]]),
          ('2020 febr. 4', [[Month(2, fn), Day(4, fn)]]),
          ('január', [[Month(1, fn)]]),
          (' február ', [[Month(2, fn)]]),
          ('janos', []),
          ('', []),
          ('2020 július', [[Month(7, fn)]]),
          ('2020 június - augusztus 30', [[Month(6, fn)], [Month(8, fn), Day(30, fn)]]),
          ('június 20 - július 30', [[Month(6, fn), Day(20, fn)], [Month(7, fn), Day(30, fn)]]),
          ('tavaly február ', [[Year(2019, fn), Month(2, fn)]]),
          ('legyen jövő február 12-én', [[Year(2021, fn), Month(2, fn), Day(12, fn)]]),
          ('legyen jövő év február 12-én', [[Year(2021, fn), Month(2, fn), Day(12, fn)]]),
          ('legyen jövőre február 12-én', [[Year(2021, fn), Month(2, fn), Day(12, fn)]])]

    for inp, exp in tf:
        out = match_named_month(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_relative_day():
    fn = 'relative_day'
    now = datetime(2020, 10, 1)

    tf = [('ma', [[Year(2020, fn), Month(10, fn), Day(1, fn)]]),
          ('ma-holnap', [[Year(2020, fn), Month(10, fn), Day(1, fn)], [Year(2020, fn), Month(10, fn), Day(2, fn)]]),
          ('holnapután reggel nyolc', [[Year(2020, fn), Month(10, fn), Day(3, fn)]]),
          ('legyen ma reggel', [[Year(2020, fn), Month(10, fn), Day(1, fn)]]),
          ('miért nem jöttél tegnap? na majd ma',
           [[Year(2020, fn), Month(10, fn), Day(1, fn)], [Year(2020, fn), Month(9, fn), Day(30, fn)]])]

    for inp, exp in tf:
        out = match_relative_day(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_weekday():
    fn = 'weekday'
    now = datetime(2020, 12, 7)  # monday

    tf = [('múlt vasárnap', [[Year(2020, fn), Month(12, fn), Day(6, fn)]]),
          ('ezen a heten hetfon', [[Year(2020, fn), Month(12, fn), Day(7, fn)]]),
          ('jövő kedden', [[Year(2020, fn), Month(12, fn), Day(15, fn)]]),
          ('előző szombaton ', [[Year(2020, fn), Month(12, fn), Day(5, fn)]]),
          ('miért nem jöttél tegnap? na majd ma', []),
          ('jövő kedden', [[Year(2020, fn), Month(12, fn), Day(15, fn)]])]

    for inp, exp in tf:
        out = match_weekday(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_match_week():
    fn = 'week'
    now = datetime(2020, 12, 7)

    tf = [('múlthéten', [[Year(2020, fn), Week(49, fn)]]),
          ('múlt hét kedden', [[Year(2020, fn), Week(49, fn)]]),
          ('ezen a heten hetfon', [[Year(2020, fn), Week(50, fn)]]),
          ('jövőhéten', [[Year(2020, fn), Week(51, fn)]]),
          ('legyen ma', [])]

    for inp, exp in tf:
        out = match_week(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_named_year():
    fn = 'named_year'
    now = datetime(2020, 12, 7)

    tf = [('tavaly', [[Year(2019, fn)]]),
          ('múlt hét kedden', []),
          ('legyen meg még idén légyszi', [[Year(2020, fn)]]),
          ('kb két év múlva', [[Year(2022, fn)]]),
          ('tavalyelőtt történt', [[Year(2018, fn)]]),
          ('40 év múlva', [[Year(2060, fn)]]),
          ('kb három évvel ezelőtt', [[Year(2017, fn)]]),
          ('találkozzunk jövő héten szombaton', [])]

    for inp, exp in tf:
        out = match_named_year(inp, now)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp
