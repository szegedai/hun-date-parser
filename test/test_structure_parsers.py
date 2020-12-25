from hun_date_parser.date_parser.structure_parsers import match_interval, match_multi_match


def test_match_interval():
    w = [('keddtől egészen péntekig', {'start_date': 'keddtől', 'end_date': 'egészen péntekig'}),
         ('reggeltől estig', {'start_date': 'reggeltől', 'end_date': 'estig'}),
         ('kedden', {}),
         ('2020 január másodikától jövő év közepéig', {'start_date': '2020 január másodikától', 'end_date': 'jövő év közepéig'}),
         ('2020 decemberétől', {'start_date': '2020 decemberétől', 'end_date': 'OPEN'}),
         ('ma reggeltől bármikor', {'start_date': 'ma reggeltől', 'end_date': 'OPEN'}),
         ('egészen péntekig jó lesz', {'start_date': 'OPEN', 'end_date': 'egészen péntekig'}),
         ('2020-10-12-től 2020-11-01-ig', {'start_date': '2020-10-12-től', 'end_date': '2020-11-01-ig'})]

    for inp, out in w:
        assert match_interval(inp) == out


def test_match_multi_match():
    w = [('kedden és szerdán', ['kedden', 'szerdán']),
         ('2020 január vagy februárjában', ['2020 január', 'februárjában'])]

    for inp, out in w:
        assert match_multi_match(inp) == out
