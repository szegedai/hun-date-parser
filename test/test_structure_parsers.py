import pytest

from hun_date_parser.date_parser.structure_parsers import match_interval, match_multi_match

interval_fixtures = [
    ('keddtől egészen péntekig', {'start_date': 'keddtől', 'end_date': 'egészen péntekig'}),
    ('reggeltől estig', {'start_date': 'reggeltől', 'end_date': 'estig'}),
    ('kedden', {}),
    ('2020 január másodikától jövő év közepéig',
     {'start_date': '2020 január másodikától', 'end_date': 'jövő év közepéig'}),
    ('2020 január másodika óta jövő év közepéig',
     {'start_date': '2020 január másodika óta', 'end_date': 'jövő év közepéig'}),
    ('2020 decemberétől', {'start_date': '2020 decemberétől', 'end_date': 'OPEN'}),
    ('2020 decembere óta', {'start_date': '2020 decembere óta', 'end_date': 'OPEN'}),
    ('január 1 óta', {'start_date': 'január 1 óta', 'end_date': 'OPEN'}),
    ('ma reggeltől bármikor', {'start_date': 'ma reggeltől', 'end_date': 'OPEN'}),
    ('egészen péntekig jó lesz', {'start_date': 'OPEN', 'end_date': 'egészen péntekig'}),
    ('2020-10-12-től 2020-11-01-ig', {'start_date': '2020-10-12-től', 'end_date': '2020-11-01-ig'}),
    ('2020-2022', {'start_date': '2020', 'end_date': '2022'}),
    ('április 1-április 11', {'start_date': 'április 1', 'end_date': 'április 11'}),
    ('2020 dec 13 - 2020 december 6', {'start_date': '2020 dec 13', 'end_date': '2020 december 6'}),
    ('2020 okt 13 - 2020 november 6', {'start_date': '2020 okt 13', 'end_date': '2020 november 6'}),
    ('2020 okt 13 - 2020 november hat', {'start_date': '2020 okt 13', 'end_date': '2020 november hat'}),
    ('márc 4 - április 6', {'start_date': 'márc 4', 'end_date': 'április 6'}),
    ('2020 június 13 -2022 április 6', {'start_date': '2020 június 13', 'end_date': '2022 április 6'}),
    ('június - július', {'start_date': 'június', 'end_date': 'július'}),
    ('jan-feb', {'start_date': 'jan', 'end_date': 'feb'}),
    ('2020 március-2022 március', {'start_date': '2020 március', 'end_date': '2022 március'}),
]


@pytest.mark.parametrize("inp, out", interval_fixtures)
def test_match_interval(inp, out):
    assert match_interval(inp) == out


def test_match_multi_match():
    w = [('kedden és szerdán', ['kedden', 'szerdán']),
         # ('kedden, szerdán és pénteken', ['kedden', 'szerdán', 'pénteken']),
         # ('kedden, szerdán', ['kedden', 'szerdán']),
         # These could cause significant unintended consequences,
         # deeper rethinking is required than simply splitting among commas as well
         ('2020 január vagy februárjában', ['2020 január', 'februárjában'])]

    for inp, out in w:
        assert match_multi_match(inp) == out
