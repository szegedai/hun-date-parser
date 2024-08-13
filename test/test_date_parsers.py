import pytest
from datetime import datetime

from hun_date_parser.date_parser.date_parsers import (Year, Month, Week, Day, OverrideTopWithNow, DayOffset,
                                                      StartDay, EndDay)
from hun_date_parser.date_parser.date_parsers import (match_iso_date, match_named_month, match_relative_day,
                                                      match_weekday,
                                                      match_week, match_named_year, match_relative_month,
                                                      match_n_periods_compared_to_now, match_in_past_n_periods,
                                                      match_date_offset, match_named_month_start_mid_end)
from hun_date_parser.utils import SearchScopes


tf_named_month = [
    ('jan 20-án', [[Month(1, 'named_month'), Day(20, 'named_month')]], SearchScopes.NOT_RESTRICTED),
    ('2020 febr. 4', [[Month(2, 'named_month'), Day(4, 'named_month')]], SearchScopes.NOT_RESTRICTED),
    ('január', [[Month(1, 'named_month')]], SearchScopes.NOT_RESTRICTED),
    (' február ', [[Month(2, 'named_month')]], SearchScopes.NOT_RESTRICTED),
    ('janos', [], SearchScopes.NOT_RESTRICTED),
    ('', [], SearchScopes.NOT_RESTRICTED),
    ('2020 július', [[Month(7, 'named_month')]], SearchScopes.NOT_RESTRICTED),
    ('2020 június - augusztus 30', [[Month(6, 'named_month')], [Month(8, 'named_month'), Day(30, 'named_month')]],
     SearchScopes.NOT_RESTRICTED),
    ('június 20 - július 30',
     [[Month(6, 'named_month'), Day(20, 'named_month')], [Month(7, 'named_month'), Day(30, 'named_month')]],
     SearchScopes.NOT_RESTRICTED),
    ('tavaly február ', [[Month(2, 'named_month'), Year(2019, 'named_month')]], SearchScopes.NOT_RESTRICTED),
    ('legyen jövő február 12-én', [[Month(2, 'named_month'), Day(12, 'named_month'), Year(2021, 'named_month')]],
     SearchScopes.NOT_RESTRICTED),
    ('legyen jövő év február 12-én', [[Month(2, 'named_month'), Day(12, 'named_month'), Year(2021, 'named_month')]],
     SearchScopes.NOT_RESTRICTED),
    ('ápr 15', [[Month(4, 'named_month'), Day(15, 'named_month')]], SearchScopes.NOT_RESTRICTED),
    ('május 15', [[Month(5, 'named_month'), Day(15, 'named_month')]], SearchScopes.NOT_RESTRICTED),
    ('április 1', [[Month(4, 'named_month'), Day(1, 'named_month')]], SearchScopes.NOT_RESTRICTED),
    ('legyen jövőre február 12-én', [[Month(2, 'named_month'), Day(12, 'named_month'), Year(2021, 'named_month')]],
     SearchScopes.NOT_RESTRICTED),
    ('május 15', [[Month(5, 'named_month'), Day(15, 'named_month'), Year(2021, 'named_month')]],
     SearchScopes.FUTURE_DAY),
    ('május 15', [[Month(5, 'named_month'), Day(15, 'named_month')]],
     SearchScopes.PAST_SEARCH),
    ('november 15', [[Month(11, 'named_month'), Day(15, 'named_month'), Year(2019, 'named_month')]],
     SearchScopes.PAST_SEARCH),
    ('október 15', [[Month(10, 'named_month'), Day(15, 'named_month')]],
     SearchScopes.FUTURE_DAY),
    ('október 15', [[Month(10, 'named_month'), Day(15, 'named_month'), Year(2019, 'named_month')]],
     SearchScopes.PAST_SEARCH),
    ('október 3', [[Month(10, 'named_month'), Day(3, 'named_month')]],
     SearchScopes.PAST_SEARCH),
    ('október 15', [[Month(10, 'named_month'), Day(15, 'named_month')]],
     SearchScopes.NOT_RESTRICTED),
    ('október 10', [[Month(10, 'named_month'), Day(10, 'named_month')]],
     SearchScopes.NOT_RESTRICTED),
    ('október 10', [[Month(10, 'named_month'), Day(10, 'named_month')]],
     SearchScopes.FUTURE_DAY),
    ('október 9', [[Month(10, 'named_month'), Day(9, 'named_month'), Year(2021, 'named_month')]],
     SearchScopes.FUTURE_DAY),
    ('október 11', [[Month(10, 'named_month'), Day(11, 'named_month'), Year(2019, 'named_month')]],
     SearchScopes.PAST_SEARCH),
    ('október', [[Month(10, 'named_month')]],
     SearchScopes.NOT_RESTRICTED),
    ('október', [[Month(10, 'named_month')]],
     SearchScopes.FUTURE_DAY),
    ('október', [[Month(10, 'named_month')]],
     SearchScopes.PAST_SEARCH),
]

tf_named_month_start_mid_end = [
    ('jan eleje', [[Month(1, 'named_month_sme'), StartDay(1, 'named_month_sme'), EndDay(10, 'named_month_sme')]], SearchScopes.NOT_RESTRICTED),
    ('2023 febr. közepe', [[Month(2, 'named_month_sme'), StartDay(10, 'named_month_sme'), EndDay(20, 'named_month_sme'), Year(2023, 'named_month_sme')]], SearchScopes.NOT_RESTRICTED),
    ('január közepén', [[Month(1, 'named_month_sme'), StartDay(10, 'named_month_sme'), EndDay(20, 'named_month_sme')]], SearchScopes.NOT_RESTRICTED),
    ('jövő január közepén', [[Month(1, 'named_month_sme'), StartDay(10, 'named_month_sme'), EndDay(20, 'named_month_sme'), Year(2021, 'named_month_sme')]], SearchScopes.NOT_RESTRICTED),
    ('2023 febr. vége', [[Month(2, 'named_month_sme'), StartDay(20, 'named_month_sme'), Year(2023, 'named_month_sme'), EndDay(28, 'named_month_sme')]], SearchScopes.NOT_RESTRICTED),
    ('2024 aug vége', [[Month(8, 'named_month_sme'), StartDay(20, 'named_month_sme'), Year(2024, 'named_month_sme'), EndDay(31, 'named_month_sme')]], SearchScopes.NOT_RESTRICTED),
    (' november közepén', [[Month(11, 'named_month_sme'), StartDay(10, 'named_month_sme'), EndDay(20, 'named_month_sme'), Year(2019, 'named_month_sme')]], SearchScopes.PAST_SEARCH),
    (' május végén', [[Month(5, 'named_month_sme'), StartDay(20, 'named_month_sme'), Year(2021, 'named_month_sme'), EndDay(31, 'named_month_sme')]], SearchScopes.FUTURE_DAY),
    (' április végén', [[Month(4, 'named_month_sme'), StartDay(20, 'named_month_sme'), Year(2021, 'named_month_sme'), EndDay(30, 'named_month_sme')]], SearchScopes.FUTURE_DAY),
]

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
    ('2020-01-15', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('legyen 2020-01 elején', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('2001-ben történt', [[Year(2001, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('2020-12-30-án', [[Year(2020, 'match_iso_date'), Month(12, 'match_iso_date'), Day(30, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('2020-12-30-án 2020.12.29',
     [[Year(2020, 'match_iso_date'), Month(12, 'match_iso_date'), Day(30, 'match_iso_date')],
      [Year(2020, 'match_iso_date'), Month(12, 'match_iso_date'), Day(29, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('2020 12 30-án', [[Year(2020, 'match_iso_date'), Month(12, 'match_iso_date'), Day(30, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('a 1 1 1 b', [], SearchScopes.NOT_RESTRICTED, None),
    ('abcd 2020 1 15 abd', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('abcd 2020. 1. 15. abd', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('abcd 2020 01 15 abd', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('2020 01 15', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('2020. 01. 15', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('2020. 01. 15.', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('15 01 2020', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('abcd 2020 01 15 10', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('ekkor: 15-01-2020', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('ekkor: 15. 01. 2020', [[Year(2020, 'match_iso_date'), Month(1, 'match_iso_date'), Day(15, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('ekkor: 01. 2020', [[Year(2020, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('ekkor 08 08 2023', [[Year(2023, 'match_iso_date'), Month(8, 'match_iso_date'), Day(8, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('ekkor 08. 08. 2023.', [[Year(2023, 'match_iso_date'), Month(8, 'match_iso_date'), Day(8, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('ekkor 2023. 08. 08. ', [[Year(2023, 'match_iso_date'), Month(8, 'match_iso_date'), Day(8, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('ekkor 2023. 08. 08 abc', [[Year(2023, 'match_iso_date'), Month(8, 'match_iso_date'), Day(8, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('ekkor 2023 08. 08 abc', [[Year(2023, 'match_iso_date'), Month(8, 'match_iso_date'), Day(8, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('ekkor 36 08 2023', [[Year(2023, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('1923 július', [[Year(1923, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, None),
    ('1923 július', [[Year(1923, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, True),
    ('1889 július', [], SearchScopes.NOT_RESTRICTED, True),
    ('1901 július', [[Year(1901, 'match_iso_date')]], SearchScopes.NOT_RESTRICTED, True),
    ('8000 forint', [], SearchScopes.NOT_RESTRICTED, True),
    ('8000', [[Year(8000, 'match_iso_date')]], SearchScopes.PAST_SEARCH, False),
    ('8000 forint', [], SearchScopes.PAST_SEARCH, False),
    ('0000', [], SearchScopes.NOT_RESTRICTED, False),
    ('0000', [], SearchScopes.NOT_RESTRICTED, True),
]

tf_weekday = [
    ('múlt vasárnap', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(6, 'weekday')]], SearchScopes.NOT_RESTRICTED),
    ('ezen a heten hetfon', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(7, 'weekday')]], SearchScopes.NOT_RESTRICTED),
    ('jövő kedden', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(15, 'weekday')]], SearchScopes.NOT_RESTRICTED),
    ('előző szombaton ', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(5, 'weekday')]], SearchScopes.NOT_RESTRICTED),
    ('miért nem jöttél tegnap? na majd ma', [], SearchScopes.NOT_RESTRICTED),
    ('jövő kedden', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(15, 'weekday')]], SearchScopes.NOT_RESTRICTED),
    ('szombaton ráérek', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(12, 'weekday')]], SearchScopes.FUTURE_DAY),
    ('mit szólnál hétfőhöz?', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(14, 'weekday')]], SearchScopes.FUTURE_DAY),
    ('pénteken ráérek', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(11, 'weekday')]], SearchScopes.FUTURE_DAY),
    ('múlt hét kedden beszéltünk', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(1, 'weekday')]], SearchScopes.FUTURE_DAY),
    ('szerdán ráérek', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(16, 'weekday')]], SearchScopes.FUTURE_DAY),
    ('jövő héten szerdán ráérek', [[Year(2020, 'weekday'), Month(12, 'weekday'), Day(16, 'weekday')]], SearchScopes.FUTURE_DAY)]

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
    ('Mik az elmúlt hónapban történtek', [[]]),
    ('a múlt hónapban időrendi sorrendben.', [[Year(2023, 'relative_month'), Month(4, 'relative_month')]]),
    (' az elmúlt hónapban a?', [[]]),
    (' az elmult honapban a?', [[]]),
    ('ebben a hónapban', [[Year(2023, 'relative_month'), Month(5, 'relative_month')]]),
    ('ezen hónapban', [[Year(2023, 'relative_month'), Month(5, 'relative_month')]]),
    ('az aktuális hónap', [[Year(2023, 'relative_month'), Month(5, 'relative_month')]]),
    ('jövő hónap', [[Year(2023, 'relative_month'), Month(6, 'relative_month')]]),
    ('következő hónap', [[Year(2023, 'relative_month'), Month(6, 'relative_month')]]),
    ('következendő hónap', [[Year(2023, 'relative_month'), Month(6, 'relative_month')]]),
]

tf_n_periods_from_now = [
    ('egy hét múlva', [[Year(2023, 'n_date_periods_compared_to_now'), Month(5, 'n_date_periods_compared_to_now'), Day(27, 'n_date_periods_compared_to_now')]]),
    ('egy héttel korábban', [[Year(2023, 'n_date_periods_compared_to_now'), Month(5, 'n_date_periods_compared_to_now'), Day(13, 'n_date_periods_compared_to_now')]]),
    ('két héttel korábbi időpont', [[Year(2023, 'n_date_periods_compared_to_now'), Month(5, 'n_date_periods_compared_to_now'), Day(6, 'n_date_periods_compared_to_now')]]),
    ('1 hét múlva', [[Year(2023, 'n_date_periods_compared_to_now'), Month(5, 'n_date_periods_compared_to_now'), Day(27, 'n_date_periods_compared_to_now')]]),
    ('1 héttel ezelőtt', [[Year(2023, 'n_date_periods_compared_to_now'), Month(5, 'n_date_periods_compared_to_now'), Day(13, 'n_date_periods_compared_to_now')]]),
    ('6 nappal ezelőtt', [[Year(2023, 'n_date_periods_compared_to_now'), Month(5, 'n_date_periods_compared_to_now'), Day(14, 'n_date_periods_compared_to_now')]]),
    ('5 nap múlva', [[Year(2023, 'n_date_periods_compared_to_now'), Month(5, 'n_date_periods_compared_to_now'), Day(25, 'n_date_periods_compared_to_now')]]),
]

tf_in_past_n_periods = [
    ("elmúlt egy hét", [[Year(2023, 'in_past_n_periods'), Month(5, 'in_past_n_periods'),
                         Day(13, 'in_past_n_periods'), OverrideTopWithNow(None, 'in_past_n_periods')]]),
    ("az előző egy hétben", [[Year(2023, 'in_past_n_periods'), Month(5, 'in_past_n_periods'),
                              Day(13, 'in_past_n_periods'), OverrideTopWithNow(None, 'in_past_n_periods')]]),
    ("az előző két hétben", [[Year(2023, 'in_past_n_periods'), Month(5, 'in_past_n_periods'),
                              Day(6, 'in_past_n_periods'), OverrideTopWithNow(None, 'in_past_n_periods')]]),
    ("az előző két évi adatok", [[Year(2021, 'in_past_n_periods'), Month(5, 'in_past_n_periods'),
                                  Day(20, 'in_past_n_periods'), OverrideTopWithNow(None, 'in_past_n_periods')]]),
    ("az előző 10 nap tranzakciói", [[Year(2023, 'in_past_n_periods'), Month(5, 'in_past_n_periods'),
                                      Day(10, 'in_past_n_periods'), OverrideTopWithNow(None, 'in_past_n_periods')]]),
    ("az előző sport nap teljesítménye", []),
]

tf_date_offset = [
    ("5 napig", [[DayOffset(5, "date_offset")]]),
    ("öt napig", [[DayOffset(5, "date_offset")]]),
    ("egy hétig", [[DayOffset(7, "date_offset")]]),
    ("3 hét", [[DayOffset(21, "date_offset")]]),
    ("az előző sport nap teljesítménye", []),
]


@pytest.mark.parametrize("inp,exp,search_scope,realistic_year_restriction", tf_iso_date)
def test_match_iso_date(inp, exp, search_scope, realistic_year_restriction):
    if realistic_year_restriction is None:
        for year_restriction in [True, False]:
            out = match_iso_date(inp, realistic_year_restriction=year_restriction)
            date_parts = []
            for e in out:
                date_parts.append(e['date_parts'])
            assert date_parts == exp
    else:
        out = match_iso_date(inp, realistic_year_restriction=realistic_year_restriction)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp

@pytest.mark.parametrize("inp,exp,search_scope", tf_named_month)
def test_named_month(inp, exp, search_scope):
    now = datetime(2020, 10, 10)

    out = match_named_month(inp, now, search_scope)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


@pytest.mark.parametrize("inp,exp,search_scope", tf_named_month_start_mid_end)
def test_named_month_start_mid_end(inp, exp, search_scope):
    now = datetime(2020, 10, 10)

    out = match_named_month_start_mid_end(inp, now, search_scope)
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


@pytest.mark.parametrize("inp,exp,search_scope", tf_weekday)
def test_match_weekday(inp, exp, search_scope):
    now = datetime(2020, 12, 11)  # friday
    out = match_weekday(inp, now, search_scope)
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
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


@pytest.mark.parametrize("inp,exp", tf_n_periods_from_now)
def test_match_n_periods_compared_to_now(inp, exp):
    now = datetime(2023, 5, 20)
    out = match_n_periods_compared_to_now(inp, now)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


@pytest.mark.parametrize("inp,exp", tf_in_past_n_periods)
def test_match_in_past_n_periods(inp, exp):
    now = datetime(2023, 5, 20)
    out = match_in_past_n_periods(inp, now)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp


@pytest.mark.parametrize("inp,exp", tf_date_offset)
def test_match_date_offset(inp, exp):
    out = match_date_offset(inp)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    assert date_parts == exp
