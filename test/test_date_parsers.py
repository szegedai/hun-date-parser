from src.date_parser.date_parsers import Year, Month, Day
from src.date_parser.date_parsers import match_iso_date, match_named_month


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
    tf = [('jan 20-án', [[Month(1), Day(20)]]),
          ('2020 febr. 4', [[Month(2), Day(4)]]),
          ('január', [[Month(1)]]),
          (' február ', [[Month(2)]]),
          ('janos', []),
          ('', []),
          ('2020 július', [[Month(7)]]),
          ('2020 június - augusztus 30', [[Month(6)], [Month(8), Day(30)]]),
          ('június 20 - július 30', [[Month(6), Day(20)], [Month(7), Day(30)]])]

    for inp, exp in tf:
        out = match_named_month(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp
