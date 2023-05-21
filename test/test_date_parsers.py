import pytest
from datetime import datetime

from hun_date_parser.date_parser.date_parsers import Year, Month, Week, Day
from hun_date_parser.date_parser.date_parsers import (match_iso_date, match_named_month, match_relative_day,
                                                      match_weekday,
                                                      match_week, match_named_year, match_relative_month)

tf_named_month = [
    ('jan 20-án', [[Month(1, 'named_month'), Day(20, 'named_month')]]),
    ('2020 febr. 4', [[Month(2, 'named_month'), Day(4, 'named_month')]]),
    ('január', [[Month(1, 'named_month')]]),
    (' február ', [[Month(2, 'named_month')]]),
    ('janos', []),
    ('', []),
    ('2020 július', [[Month(7, 'named_month')]]),
    ('2020 június - augusztus 30', [[Month(6, 'named_month')], [Month(8, 'named_month'), Day(30, 'named_month')]]),
    ('június 20 - július 30',
     [[Month(6, 'named_month'), Day(20, 'named_month')], [Month(7, 'named_month'), Day(30, 'named_month')]]),
    ('tavaly február ', [[Year(2019, 'named_month'), Month(2, 'named_month')]]),
    ('legyen jövő február 12-én', [[Year(2021, 'named_month'), Month(2, 'named_month'), Day(12, 'named_month')]]),
    ('legyen jövő év február 12-én', [[Year(2021, 'named_month'), Month(2, 'named_month'), Day(12, 'named_month')]]),
    ('ápr 15', [[Month(4, 'named_month'), Day(15, 'named_month')]]),
    ('május 15', [[Month(5, 'named_month'), Day(15, 'named_month')]]),
    ('április 1', [[Month(4, 'named_month'), Day(1, 'named_month')]]),
    ('legyen jövőre február 12-én', [[Year(2021, 'named_month'), Month(2, 'named_month'), Day(12, 'named_month')]])]

tf_match_relative_day = [
    ('ma', [[Year(2020, 'relative_day'), Month(10, 'relative_day'), Day(1, 'relative_day')]]),
    ('ma-holnap', [[Year(2020, 'relative_day'), Month(10, 'relative_day'), Day(1, 'relative_day')],
                   [Year(2020, 'relative_day'), Month(10, 'relative_day'), Day(2, 'relative_day')]]),
    ('holnapután reggel nyolc', [[Year(2020, 'relative_day'), Month(10, 'relative_day'), Day(3, 'relative_day')]]),
    ('legyen ma reggel', [[Year(2020, 'relative_day'), Month(10, 'relative_day'), Day(1, 'relative_day')]]),
    ('miért nem jöttél tegnap? na majd ma',
     [[Year(2020, 'relative_day'), Month(10, 'relative_day'), Day(1, 'relative_day')],
      [Year(2020, 'relative_day'), Month(9, 'relative_day'), Day(30, 'relative_day')]])
]

tf_iso_date = [
    ('2020-01-15', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]]),
    ('legyen 2020-01 elején', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date')]]),
    ('2001-ben történt', [[Year(2001, 'match_iso_date')]]),
    ('2020-12-30-án', [[Year(2020, 'match_iso_date'), Month(12, 'match_iso_date'), Day(30, 'match_iso_date')]]),
    ('2020-12-30-án 2020.12.29',
     [[Year(2020, 'match_iso_date'), Month(12, 'match_iso_date'), Day(30, 'match_iso_date')],
      [Year(2020, 'match_iso_date'), Month(12, 'match_iso_date'), Day(29, 'match_iso_date')]])]

tf_weekday = [
    ('múlt vasárnap', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(6, 'weekday')]], False),
    ('ezen a heten hetfon', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(7, 'weekday')]], False),
    ('jövő kedden', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(15, 'weekday')]], False),
    ('előző szombaton ', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(5, 'weekday')]], False),
    ('miért nem jöttél tegnap? na majd ma', [], False),
    ('jövő kedden', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(15, 'weekday')]], False),
    ('szombaton ráérek', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(12, 'weekday')]], True),
    ('mit szólnál hétfőhöz?', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(14, 'weekday')]], True),
    ('pénteken ráérek', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(11, 'weekday')]], True),
    ('múlt hét kedden beszéltünk', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(1, 'weekday')]], True),
    ('szerdán ráérek', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(16, 'weekday')]], True),
    ('jövő héten szerdán ráérek', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(16, 'weekday')]], True)]

tf_week = [('múlthéten', [[Year(2020, "week"), Week(49, "week")]]),
           ('múlt hét kedden', [[Year(2020, "week"), Week(49, "week")]]),
           ('ezen a heten hetfon', [[Year(2020, "week"), Week(50, "week")]]),
           ('jövőhéten', [[Year(2020, "week"), Week(51, "week")]]),
           ('legyen ma', [])]

tf_named_year = [('tavaly', [[Year(2019, 'named_year')]]),
                 ('múlt hét kedden', []),
                 ('legyen meg még idén légyszi', [[Year(2020, 'named_year')]]),
                 ('kb két év múlva', [[Year(2022, 'named_year')]]),
                 ('tavalyelőtt történt', [[Year(2018, 'named_year')]]),
                 ('40 év múlva', [[Year(2060, 'named_year')]]),
                 ('kb három évvel ezelőtt', [[Year(2017, 'named_year')]]),
                 ('találkozzunk jövő héten szombaton', [])]

tf_relative_month = [
    ('az utolsó hónapom.', [[Year(2023, 'relative_month'), Month(4, 'relative_month')]]),
    ('a legutóbbi hónapom.', [[Year(2023, 'relative_month'), Month(4, 'relative_month')]]),
    ('a legutobbi honapom', [[Year(2023, 'relative_month'), Month(4, 'relative_month')]]),
    ('mi történt a múlt hónapban?', [[Year(2023, 'relative_month'), Month(4, 'relative_month')]]),
    ('Mik az elmúlt hónapban történtek', [[Year(2023, 'relative_month'), Month(4, 'relative_month')]]),
    ('a múlt hónapban időrendi sorrendben.', [[Year(2023, 'relative_month'), Month(4, 'relative_month')]]),
    (' az elmúlt hónapban a?', [[Year(2023, 'relative_month'), Month(4, 'relative_month')]]),
    (' az elmult honapban a?', [[Year(2023, 'relative_month'), Month(4, 'relative_month')]]),
    ('ebben a hónapban', [[Year(2023, 'relative_month'), Month(5, 'relative_month')]]),
    ('ezen hónapban', [[Year(2023, 'relative_month'), Month(5, 'relative_month')]]),
    ('az aktuális hónap', [[Year(2023, 'relative_month'), Month(5, 'relative_month')]]),
    ('jövő hónap', [[Year(2023, 'relative_month'), Month(6, 'relative_month')]]),
    ('következő hónap', [[Year(2023, 'relative_month'), Month(6, 'relative_month')]]),
    ('következendő hónap', [[Year(2023, 'relative_month'), Month(6, 'relative_month')]]),
]


@pytest.mark.parametrize("inp,exp", tf_iso_date)
def test_match_iso_date(inp, exp):
    out = match_iso_date(inp)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


@pytest.mark.parametrize("inp,exp", tf_named_month)
def test_named_month(inp, exp):
    now = datetime(2020, 10, 1)

    out = match_named_month(inp, now)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


@pytest.mark.parametrize("inp,exp", tf_match_relative_day)
def test_match_relative_day(inp, exp):
    now = datetime(2020, 10, 1)

    out = match_relative_day(inp, now)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


@pytest.mark.parametrize("inp,exp,expect_future_day", tf_weekday)
def test_match_weekday(inp, exp, expect_future_day):
    now = datetime(2020, 12, 11)  # friday
    out = match_weekday(inp, now, expect_future_day)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


@pytest.mark.parametrize("inp,exp", tf_week)
def test_match_match_week(inp, exp):
    now = datetime(2020, 12, 7)
    out = match_week(inp, now)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


@pytest.mark.parametrize("inp,exp", tf_named_year)
def test_match_named_year(inp, exp):
    now = datetime(2020, 12, 7)
    out = match_named_year(inp, now)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp

@pytest.mark.parametrize("inp,exp", tf_relative_month)
def test_match_relative_month(inp, exp):
    now = datetime(2023, 5, 20)
    out = match_relative_month(inp, now)
    print(out)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp
