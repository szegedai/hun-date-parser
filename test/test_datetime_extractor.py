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
    ("holnaptól 5 napig", [datetime(2020, 12, 19), datetime(2020, 12, 24, 23, 59, 59)]),
    ("holnaptól öt napig", [datetime(2020, 12, 19), datetime(2020, 12, 24, 23, 59, 59)]),
    ("dec 20-tól 4 napig", [datetime(2020, 12, 20), datetime(2020, 12, 24, 23, 59, 59)]),
    ("5 napig holnaptól", [datetime(2020, 12, 19), datetime(2020, 12, 24, 23, 59, 59)]),
    ("3 fő, 4 csillagos szálloda, 5 napig holnaptól", [datetime(2020, 12, 19), datetime(2020, 12, 24, 23, 59, 59)]),
    ("a válasz: 5 napra holnaptól", [datetime(2020, 12, 19), datetime(2020, 12, 24, 23, 59, 59)]),
    (" öt napig holnaptól", [datetime(2020, 12, 19), datetime(2020, 12, 24, 23, 59, 59)]),
    ("nagy kalandra megyek 4 napig dec 20-tól ", [datetime(2020, 12, 20), datetime(2020, 12, 24, 23, 59, 59)]),
    ("nagy kalandra megyek 4 napig vasárnaptól ", [datetime(2020, 12, 20), datetime(2020, 12, 24, 23, 59, 59)]),
    ("a konferencia holnap kezdődik és 5 napig tart", [datetime(2020, 12, 19), datetime(2020, 12, 24, 23, 59, 59)]),
    ("a konferencia holnap kezdődik és 5 napos tart", [datetime(2020, 12, 19), datetime(2020, 12, 24, 23, 59, 59)]),
    ("a konferencia holnap indul és öt napig tart", [datetime(2020, 12, 19), datetime(2020, 12, 24, 23, 59, 59)]),
    ("egy hétig tart holnaptól", [datetime(2020, 12, 19), datetime(2020, 12, 26, 23, 59, 59)]),
    ("holnaptól egy hétig", [datetime(2020, 12, 19), datetime(2020, 12, 26, 23, 59, 59)]),
    ("holnaptól két hétig", [datetime(2020, 12, 19), datetime(2021, 1, 2, 23, 59, 59)]),
    ("holnapi naptól két hétig", [datetime(2020, 12, 19), datetime(2021, 1, 2, 23, 59, 59)]),
    ("holnaptól kezdődően két hétig", [datetime(2020, 12, 19), datetime(2021, 1, 2, 23, 59, 59)]),
    ("holnap indulunk és két hétig tart", [datetime(2020, 12, 19), datetime(2021, 1, 2, 23, 59, 59)]),
    ("holnapi indulással két hétig", [datetime(2020, 12, 19), datetime(2021, 1, 2, 23, 59, 59)]),
    ("vasárnapi kezdéssel 2 hétig", [datetime(2020, 12, 20), datetime(2021, 1, 3, 23, 59, 59)]),
    ("dec 20-tól 30-ig", [datetime(2020, 12, 20), datetime(2020, 12, 30, 23, 59, 59)]),
    ("dec 20-dec 30", [datetime(2020, 12, 20), datetime(2020, 12, 30, 23, 59, 59)]),
    ("április 1-április 11", [datetime(2020, 4, 1), datetime(2020, 4, 11, 23, 59, 59)]),
    ("2020 április 1-2020 április 11", [datetime(2020, 4, 1), datetime(2020, 4, 11, 23, 59, 59)]),
    ("2020 április - 2020 május", [datetime(2020, 4, 1), datetime(2020, 5, 31, 23, 59, 59)]),
    ("2020-2022", [datetime(2020, 1, 1), datetime(2022, 12, 31, 23, 59, 59)]),
    ("augusztus 5-től 10-ig", [datetime(2020, 8, 5), datetime(2020, 8, 10, 23, 59, 59)]),
    ("augusztus 5-től 10-ig 2-en megyünk", [datetime(2020, 8, 5), datetime(2020, 8, 10, 23, 59, 59)]),
    (" 2-en megyünk augusztus 5-től 10-ig", [datetime(2020, 8, 5), datetime(2020, 8, 10, 23, 59, 59)]),
    ("február 13-tól 17-ig", [datetime(2020, 2, 13), datetime(2020, 2, 17, 23, 59, 59)]),
    ("Kezdő dátum: február 13., végzés dátuma: február 17.", [datetime(2020, 2, 13), datetime(2020, 2, 17, 23, 59, 59)]),
    ("Induló dátum: február 13., záró dátuma: február 17.", [datetime(2020, 2, 13), datetime(2020, 2, 17, 23, 59, 59)]),
    ("kezdeti dátum: február 13 eddig tart: február 17", [datetime(2020, 2, 13), datetime(2020, 2, 17, 23, 59, 59)]),
    ("kezdet: február 13 eddig: feb 17.", [datetime(2020, 2, 13), datetime(2020, 2, 17, 23, 59, 59)]),
    ("február három", [datetime(2020, 2, 3), datetime(2020, 2, 3, 23, 59, 59)]),
    ("február harmadika", [datetime(2020, 2, 3), datetime(2020, 2, 3, 23, 59, 59)]),
    ("február elseje", [datetime(2020, 2, 1), datetime(2020, 2, 1, 23, 59, 59)]),
    ("március elsején", [datetime(2020, 3, 1), datetime(2020, 3, 1, 23, 59, 59)]),
    ("március tizenegy", [datetime(2020, 3, 11), datetime(2020, 3, 11, 23, 59, 59)]),
    ("március tizenegytől április elsejéig", [datetime(2020, 3, 11), datetime(2020, 4, 1, 23, 59, 59)]),
    ("tavalyi események", [datetime(2019, 1, 1), datetime(2019, 12, 31, 23, 59, 59)]),
    ("a tavalyi események", [datetime(2019, 1, 1), datetime(2019, 12, 31, 23, 59, 59)]),
    ("a tavaly történtek", [datetime(2019, 1, 1), datetime(2019, 12, 31, 23, 59, 59)]),
    ("idei események", [datetime(2020, 1, 1), datetime(2020, 12, 31, 23, 59, 59)]),
    ("az idei események", [datetime(2020, 1, 1), datetime(2020, 12, 31, 23, 59, 59)]),
    ("az idén történtek", [datetime(2020, 1, 1), datetime(2020, 12, 31, 23, 59, 59)]),
    ("az ebben az évben történtek", [datetime(2020, 1, 1), datetime(2020, 12, 31, 23, 59, 59)]),
    ("bejövő hívás májusban", [datetime(2020, 5, 1), datetime(2020, 5, 31, 23, 59, 59)]),
    ("jövök májusban", [datetime(2020, 5, 1), datetime(2020, 5, 31, 23, 59, 59)]),
    (" május óta", [datetime(2020, 5, 1), None]),
    (" május 5 óta", [datetime(2020, 5, 5), None]),
    (" majus 5 ota", [datetime(2020, 5, 5), None]),
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

    ([Month(10, "rule_name"), StartDay(1, "rule_name"), EndDay(10, "rule_name")], datetime(2023, 10, 1, 0, 0, 0), True),
    ([Month(10, "rule_name"), StartDay(1, "rule_name"), EndDay(10, "rule_name")], datetime(2023, 10, 10, 23, 59, 59), False),

    ([Month(5, "rule_name"), StartDay(10, "rule_name"), EndDay(20, "rule_name")], datetime(2023, 5, 10, 0, 0, 0), True),
    ([Month(5, "rule_name"), StartDay(10, "rule_name"), EndDay(20, "rule_name")], datetime(2023, 5, 20, 23, 59, 59), False),

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
    ("augusztus 11-től 17-ig", [datetime(2023, 8, 11, 0, 0, 0), datetime(2023, 8, 17, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("május 11-től 17-ig", [datetime(2023, 5, 11, 0, 0, 0), datetime(2023, 5, 17, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("május 11-től 17-ig", [datetime(2023, 5, 11, 0, 0, 0), datetime(2023, 5, 17, 23, 59, 59)], SearchScopes.NOT_RESTRICTED),
    # ("augusztus 11-től 17-ig", [datetime(2022, 8, 11, 0, 0, 0), datetime(2022, 8, 17, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    # TODO: add search scope support to named_month_interval rule
    ("augusztus 11-től szeptember 17-ig", [datetime(2022, 8, 11, 0, 0, 0), datetime(2022, 9, 17, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("kezdő dátum: augusztus 11 eddig: szeptember 17-ig", [datetime(2022, 8, 11, 0, 0, 0), datetime(2022, 9, 17, 23, 59, 59)], SearchScopes.PAST_SEARCH),
    ("kezdő dátum: augusztus 11 eddig: szeptember 17-ig", [datetime(2023, 8, 11, 0, 0, 0), datetime(2023, 9, 17, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("augusztus eleje", [datetime(2023, 8, 1, 0, 0, 0), datetime(2023, 8, 10, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("augusztus eleji", [datetime(2023, 8, 1, 0, 0, 0), datetime(2023, 8, 10, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("augusztus vége", [datetime(2023, 8, 20, 0, 0, 0), datetime(2023, 8, 31, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("2022 április vége", [datetime(2022, 4, 20, 0, 0, 0), datetime(2022, 4, 30, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("jövő április vége", [datetime(2024, 4, 20, 0, 0, 0), datetime(2024, 4, 30, 23, 59, 59)], SearchScopes.FUTURE_DAY),
    ("jövő április vége", [datetime(2024, 4, 20, 0, 0, 0), datetime(2024, 4, 30, 23, 59, 59)], SearchScopes.NOT_RESTRICTED),
    ("2020 április közepi", [datetime(2020, 4, 10, 0, 0, 0), datetime(2020, 4, 20, 23, 59, 59)], SearchScopes.NOT_RESTRICTED),
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
    "június 31",
    "március 32-től április 35-ig",
    "május 5-től április 3-ig"
]


@pytest.mark.parametrize("inp_txt", tf_bad_dates)
def test_bad_dates(inp_txt):
    now = datetime(2023, 6, 1)
    de = DatetimeExtractor(now)
    parsed_date = de.parse_datetime(inp_txt)
    assert parsed_date == []


tf_partial_bad_dates = [
    ("március 32-től április elsejéig", [None, datetime(2023, 4, 1, 23, 59, 59)]),
]


@pytest.mark.parametrize("inp_txt, resp", tf_partial_bad_dates)
def test_partial_bad_dates(inp_txt, resp):
    st, end = resp
    now = datetime(2023, 6, 1)
    de = DatetimeExtractor(now)
    parsed_date = de.parse_datetime(inp_txt)
    assert len(parsed_date) == 1
    assert parsed_date[0]["start_date"] == st
    assert parsed_date[0]["end_date"] == end
