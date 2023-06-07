import pytest
from datetime import datetime

from hun_date_parser.utils import *
from hun_date_parser.date_parser.datetime_extractor import DatetimeExtractor, extend_start_end

scenarios = [
    ('ezen a héten', [datetime(2020, 12, 14, 0, 0, 0), datetime(2020, 12, 20, 23, 59, 59)]),
    ('legyen ma reggel nyolckor', [datetime(2020, 12, 18, 8, 0, 0), datetime(2020, 12, 18, 8, 59, 59)]),
    ('legyen ma', [datetime(2020, 12, 18, 0, 0, 0), datetime(2020, 12, 18, 23, 59, 59)]),
    ('találkozzunk szombaton reggel háromnegyed nyolckor', [datetime(2020, 12, 19, 7, 45, 0),
                                                            datetime(2020, 12, 19, 7, 45, 59)]),
    ('találkozzunk szombaton háromnegyed nyolckor', [datetime(2020, 12, 19, 7, 45, 0),
                                                     datetime(2020, 12, 19, 7, 45, 59)]),
    ('találkozzunk december 27-én', [datetime(2020, 12, 27), datetime(2020, 12, 27, 23, 59, 59)]),
    ('találkozzunk december 10-én', [datetime(2020, 12, 10), datetime(2020, 12, 10, 23, 59, 59)]),
    ('találkozzunk jövő héten kedden', [datetime(2020, 12, 22), datetime(2020, 12, 22, 23, 59, 59)]),
    ('találkozzunk jövő héten kedden reggel nyolckor', [datetime(2020, 12, 22, 8), datetime(2020, 12, 22, 8, 59, 59)]),
    ('ráérek jövő hét hétfőn', [datetime(2020, 12, 21), datetime(2020, 12, 21, 23, 59, 59)]),
    ('ráérek jövő hét hétfőn reggel 7-kor', [datetime(2020, 12, 21, 7), datetime(2020, 12, 21, 7, 59, 59)]),
    ('ráérek jövő hét hétfőn reggel hétkor', [datetime(2020, 12, 21, 7), datetime(2020, 12, 21, 7, 59, 59)]),
    ('ráérek jövő hétfőn reggel hétkor', [datetime(2020, 12, 21, 7), datetime(2020, 12, 21, 7, 59, 59)]),
    ('ráérek reggel hétkor', [datetime(2020, 12, 18, 7), datetime(2020, 12, 18, 7, 59, 59)]),
    ('hétfőn reggel hétkor', [datetime(2020, 12, 14, 7), datetime(2020, 12, 14, 7, 59, 59)]),
    ('reggel hétkor', [datetime(2020, 12, 18, 7), datetime(2020, 12, 18, 7, 59, 59)]),
    ('hétkor', [datetime(2020, 12, 18, 19), datetime(2020, 12, 18, 19, 59, 59)]),
    ('2021 január 5', [datetime(2021, 1, 5), datetime(2021, 1, 5, 23, 59, 59)]),
    ('2021 január 5 reggel 7', [datetime(2021, 1, 5, 7), datetime(2021, 1, 5, 7, 59, 59)]),
    ('január 5 reggel 7', [datetime(2020, 1, 5, 7), datetime(2020, 1, 5, 7, 59, 59)]),
    ('január 5-én', [datetime(2020, 1, 5), datetime(2020, 1, 5, 23, 59, 59)]),
    ('legyen most mondjuk', [datetime(2020, 12, 18), datetime(2020, 12, 18, 0, 0, 59)]),  # TODO: Come up with better
    ('egy óra múlva', [datetime(2020, 12, 18, 1), datetime(2020, 12, 18, 1, 59, 59)]),
    ('két óra múlva', [datetime(2020, 12, 18, 2), datetime(2020, 12, 18, 2, 59, 59)]),
    ('egy hét múlva', [datetime(2020, 12, 25), datetime(2020, 12, 25, 23, 59, 59)]),
    ('5 perc múlva', [datetime(2020, 12, 18, 0, 5), datetime(2020, 12, 18, 0, 5, 59)]),
    ('három nap múlva', [datetime(2020, 12, 21), datetime(2020, 12, 21, 23, 59, 59)]),
    ('csütörtök', [datetime(2020, 12, 17), datetime(2020, 12, 17, 23, 59, 59)]),
    ('jövő csütörtökön', [datetime(2020, 12, 24), datetime(2020, 12, 24, 23, 59, 59)]),
    ('jövő csütörtökön 16h', [datetime(2020, 12, 24, 16), datetime(2020, 12, 24, 16, 59, 59)]),
    ('igen 10-kor', [datetime(2020, 12, 18, 10), datetime(2020, 12, 18, 10, 59, 59)]),
    ('csütörtök vagy péntek', [datetime(2020, 12, 17), datetime(2020, 12, 17, 23, 59, 59),
                               datetime(2020, 12, 18), datetime(2020, 12, 18, 23, 59, 59)]),
    ('előző két napban', [datetime(2020, 12, 16), datetime(2020, 12, 18)]),
    ('előző 14 napban', [datetime(2020, 12, 4), datetime(2020, 12, 18)]),
    ('előző tizennégy napban', [datetime(2020, 12, 4), datetime(2020, 12, 18)]),
    ('előző 1 havi', [datetime(2020, 11, 18), datetime(2020, 12, 18)]),
    ('előző 2 havi', [datetime(2020, 10, 18), datetime(2020, 12, 18)]),
    ('előző két havi', [datetime(2020, 10, 18), datetime(2020, 12, 18)]),
    ('előző két hónapban', [datetime(2020, 10, 18), datetime(2020, 12, 18)]),
    ('megelőző két hónap', [datetime(2020, 10, 18), datetime(2020, 12, 18)]),
    ('elmúlt két hónap', [datetime(2020, 10, 18), datetime(2020, 12, 18)]),
    ('az elmúlt két hónap', [datetime(2020, 10, 18), datetime(2020, 12, 18)]),
    ('az elmúlt két hónap', [datetime(2020, 10, 18), datetime(2020, 12, 18)]),
    ('az elmúlt hónap', [datetime(2020, 11, 18), datetime(2020, 12, 18)]),
    ('az elmúlt nap', [datetime(2020, 12, 17), datetime(2020, 12, 18)]),
    ('az elmúlt 1 nap', [datetime(2020, 12, 17), datetime(2020, 12, 18)]),
    ('az elmúlt egy nap', [datetime(2020, 12, 17), datetime(2020, 12, 18)]),
    ('az elmúlt hét', [datetime(2020, 12, 11), datetime(2020, 12, 18)]),
    ('az elmúlt 1 hét', [datetime(2020, 12, 11), datetime(2020, 12, 18)]),
]


@pytest.mark.parametrize("inp_txt, resp", scenarios)
def test_datetime_extractor(inp_txt, resp):
    now = datetime(2020, 12, 18)
    de = DatetimeExtractor(now)
    parsed_date = de.parse_datetime(inp_txt)

    if len(resp) == 2:
        st, end = resp

        assert len(parsed_date) == 1
        assert parsed_date[0]['start_date'] == st
        assert parsed_date[0]['end_date'] == end

    elif len(resp) == 4:
        st1, end1, st2, end2 = resp

        assert len(parsed_date) == 2
        assert parsed_date[0]['start_date'] == st1
        assert parsed_date[0]['end_date'] == end1
        assert parsed_date[1]['start_date'] == st2
        assert parsed_date[1]['end_date'] == end2


def test_extend_start_end():
    inp_1 = {'start_date': [], 'end_date': [Hour(1, '')]}
    assert extend_start_end(inp_1) == inp_1

    inp_2 = {'start_date': [Month(1, ''), Hour(1, '')], 'end_date': []}
    assert extend_start_end(inp_2) == {'start_date': [Month(1, ''), Hour(1, '')],
                                       'end_date': [Month(1, ''), Hour(1, '')]}


assemble_scenarios = [
    ([Year(2024, "rule_name"), Month(2, "rule_name")], datetime(2024, 2, 1, 0, 0, 0), True),
    ([Year(2024, "rule_name"), Month(2, "rule_name")], datetime(2024, 2, 29, 23, 59, 59), False),

    ([Year(2024, "rule_name"), Month(2, "rule_name"), Day(2, "rule_name")], datetime(2024, 2, 2, 0, 0, 0), True),
    ([Year(2024, "rule_name"), Month(2, "rule_name"), Day(2, "rule_name")], datetime(2024, 2, 2, 23, 59, 59), False),

    ([Month(7, "rule_name"), Day(2, "rule_name")], datetime(2023, 7, 2, 0, 0, 0), True),
    ([Month(7, "rule_name"), Day(2, "rule_name")], datetime(2023, 7, 2, 23, 59, 59), False),

    ([Day(29, "rule_name"), Hour(10, "rule_name")], datetime(2023, 5, 29, 10, 0, 0), True),
    ([Day(29, "rule_name"), Hour(10, "rule_name")], datetime(2023, 5, 29, 10, 59, 59), False),

    ([Hour(10, "rule_name")], datetime(2023, 5, 23, 10, 0, 0), True),

    ([Hour(12, "rule_name"), OverrideBottomWithNow(None, "rule_name")], datetime(2023, 5, 23, 12, 59, 59), False),
    ([Hour(12, "rule_name"), OverrideBottomWithNow(None, "rule_name")], datetime(2023, 5, 23, 0, 0, 0), True),
    ([Year(2023, "rule_name"), Month(5, "rule_name"), Day(22, "rule_name"), Hour(12, "rule_name"),
      OverrideTopWithNow(None, "rule_name")], datetime(2023, 5, 22, 12, 0, 0), True),
    ([Year(2023, "rule_name"), Month(5, "rule_name"), Day(22, "rule_name"), Hour(12, "rule_name"),
      OverrideTopWithNow(None, "rule_name")], datetime(2023, 5, 23, 0, 0, 0), False),
]


@pytest.mark.parametrize("inp_lst, resp, is_bottom", assemble_scenarios)
def test_assemble_datetime(inp_lst, resp, is_bottom):
    now = datetime(2023, 5, 23)
    dt_extractor = DatetimeExtractor()
    result = dt_extractor.assemble_datetime(now=now,
                                            dateparts=inp_lst,
                                            bottom=is_bottom)

    assert result == resp


tf_past_search_scenarios = [
    ('ezen a héten', [datetime(2023, 5, 29, 0, 0, 0), datetime(2023, 6, 4, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ('ezen a héten', [datetime(2023, 5, 29, 0, 0, 0), datetime(2023, 6, 4, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ('legyen ma reggel nyolckor', [datetime(2023, 6, 1, 8, 0, 0), datetime(2023, 6, 1, 8, 59, 59)],
     SearchScopes.PAST_SEARCH),
    ('legyen ma', [datetime(2023, 6, 1, 0, 0, 0), datetime(2023, 6, 1, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ('legyen ma', [datetime(2023, 6, 1, 0, 0, 0), datetime(2023, 6, 1, 23, 59, 59)], SearchScopes.NOT_RESTRICTED),
    ('legyen ma', [datetime(2023, 6, 1, 0, 0, 0), datetime(2023, 6, 1, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("szombat", [datetime(2023, 5, 27, 0, 0, 0), datetime(2023, 5, 27, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("szombat", [datetime(2023, 6, 3, 0, 0, 0), datetime(2023, 6, 3, 23, 59, 59)], SearchScopes.NOT_RESTRICTED),
    ("szombat", [datetime(2023, 6, 3, 0, 0, 0), datetime(2023, 6, 3, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("múlt szombat", [datetime(2023, 5, 27, 0, 0, 0), datetime(2023, 5, 27, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("csütörtök", [datetime(2023, 6, 1, 0, 0, 0), datetime(2023, 6, 1, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("csütörtök", [datetime(2023, 6, 1, 0, 0, 0), datetime(2023, 6, 1, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("csütörtök", [datetime(2023, 6, 1, 0, 0, 0), datetime(2023, 6, 1, 23, 59, 59)], SearchScopes.NOT_RESTRICTED),
    ("szerda", [datetime(2023, 5, 31, 0, 0, 0), datetime(2023, 5, 31, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("múlt szerda", [datetime(2023, 5, 24, 0, 0, 0), datetime(2023, 5, 24, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("múlt szerda", [datetime(2023, 5, 24, 0, 0, 0), datetime(2023, 5, 24, 23, 59, 59)], SearchScopes.NOT_RESTRICTED),
    ("múlt szerda", [datetime(2023, 5, 24, 0, 0, 0), datetime(2023, 5, 24, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("kedd", [datetime(2023, 5, 30, 0, 0, 0), datetime(2023, 5, 30, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("kedd", [datetime(2023, 5, 30, 0, 0, 0), datetime(2023, 5, 30, 23, 59, 59)], SearchScopes.NOT_RESTRICTED),
    ("kedd", [datetime(2023, 6, 6, 0, 0, 0), datetime(2023, 6, 6, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("hétfő", [datetime(2023, 6, 5, 0, 0, 0), datetime(2023, 6, 5, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("jövő hétfő", [datetime(2023, 6, 5, 0, 0, 0), datetime(2023, 6, 5, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("jövő hétfő", [datetime(2023, 6, 5, 0, 0, 0), datetime(2023, 6, 5, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("augusztus", [datetime(2022, 8, 1, 0, 0, 0), datetime(2022, 8, 31, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("augusztus", [datetime(2023, 8, 1, 0, 0, 0), datetime(2023, 8, 31, 23, 59, 59)], SearchScopes.NOT_RESTRICTED),
    ("augusztus", [datetime(2023, 8, 1, 0, 0, 0), datetime(2023, 8, 31, 23, 59, 59)], SearchScopes.FUTURE_DAY),
]


@pytest.mark.parametrize("inp_txt, resp, search_scope", tf_past_search_scenarios)
def test_past_search(inp_txt, resp, search_scope):
    now = datetime(2023, 6, 1)
    de = DatetimeExtractor(now, search_scope=search_scope)
    parsed_date = de.parse_datetime(inp_txt)
    st, end = resp

    assert len(parsed_date) == 1
    assert parsed_date[0]['start_date'] == st
    assert parsed_date[0]['end_date'] == end


tf_bad_dates = [
    "január 32",
    "június 31"
]


@pytest.mark.parametrize("inp_txt", tf_bad_dates)
def test_bad_dates(inp_txt):
    now = datetime(2023, 6, 1)
    de = DatetimeExtractor(now)
    parsed_date = de.parse_datetime(inp_txt)
    assert parsed_date == []

