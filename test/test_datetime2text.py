from datetime import time

from hun_date_parser.date_textualizer.time2text import time2lifelike


def test_time2lifelike():
    tf = [(time(22, 50), 'éjjel háromnegyed 11 után 5 perccel'),
          (time(23, 44), 'éjjel háromnegyed 12 előtt 1 perccel'),
          (time(8, 0), 'reggel 8 óra'),
          (time(0), 'éjjel 12 óra'),
          (time(10, 59), 'délelőtt 11 óra előtt 1 perccel'),
          (time(4, 4), 'hajnal 4 óra után 4 perccel'),
          (time(2, 16), 'éjjel negyed 3 után 1 perccel'),
          (time(12), '12 óra'),
          (time(11, 45), 'háromnegyed 12')]

    for inp, out in tf:
        assert time2lifelike(inp) == out
