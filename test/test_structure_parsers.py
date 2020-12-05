from src.structure_parsers import match_interval


def test_match_interval():
    w = [('keddtől egészen péntekig', {'start_date': 'keddtől', 'end_date': 'egészen péntekig'}),
         ('reggeltől estig', {'start_date': 'reggeltől', 'end_date': 'estig'}),
         ('kedden', {}),
         ('2020 január másodikától jövő év közepéig', {'start_date': '2020 január másodikától', 'end_date': 'jövő év közepéig'}),
         ('2020 decemberétől', {'start_date': '2020 decemberétől', 'end_date': 'OPEN'}),
         ('ma reggeltől bármikor', {'start_date': 'ma reggeltől', 'end_date': 'OPEN'}),
         ('egészen péntekig jó lesz', {'start_date': 'OPEN', 'end_date': 'egészen péntekig'})]

    for inp, out in w:
        assert match_interval(inp) == out
