from datetime import datetime

from hun_date_parser.utils import *
from hun_date_parser.date_parser.datetime_extractor import DatetimeExtractor, extend_start_end


def test_datetime_extractor():
    tf = [
        ('ezen a héten', datetime(2020, 12, 14, 0, 0, 0), datetime(2020, 12, 20, 23, 59, 59)),
        ('legyen ma reggel nyolckor', datetime(2020, 12, 18, 8, 0, 0), datetime(2020, 12, 18, 8, 59, 59)),
        ('legyen ma', datetime(2020, 12, 18, 0, 0, 0), datetime(2020, 12, 18, 23, 59, 59)),
        ('találkozzunk szombaton háromnegyed nyolckor', datetime(2020, 12, 19, 7, 45, 0),
         datetime(2020, 12, 19, 7, 45, 59)),
        ('találkozzunk szombaton háromnegyed nyolc előtt két perccel', datetime(2020, 12, 19, 7, 43, 0),
         datetime(2020, 12, 19, 7, 43, 59)),
        ('találkozzunk december 27-én', datetime(2020, 12, 27), datetime(2020, 12, 27, 23, 59, 59)),
        ('találkozzunk december 10-én', datetime(2020, 12, 10), datetime(2020, 12, 10, 23, 59, 59)),
        ('találkozzunk jövő héten kedden', datetime(2020, 12, 22), datetime(2020, 12, 22, 23, 59, 59)),
        ('találkozzunk jövő héten kedden reggel nyolckor', datetime(2020, 12, 22, 8), datetime(2020, 12, 22, 8, 59, 59)),
        ('ráérek jövő hét hétfőn', datetime(2020, 12, 21), datetime(2020, 12, 21, 23, 59, 59)),
        ('ráérek jövő hét hétfőn reggel 7-kor', datetime(2020, 12, 21, 7), datetime(2020, 12, 21, 7, 59, 59)),
        ('ráérek jövő hét hétfőn reggel hétkor', datetime(2020, 12, 21, 7), datetime(2020, 12, 21, 7, 59, 59)),
        ('ráérek jövő hétfőn reggel hétkor', datetime(2020, 12, 21, 7), datetime(2020, 12, 21, 7, 59, 59)),
        ('ráérek reggel hétkor', datetime(2020, 12, 18, 7), datetime(2020, 12, 18, 7, 59, 59)),
        ('hétfőn hétkor', datetime(2020, 12, 14, 7), datetime(2020, 12, 14, 7, 59, 59)),
        ('hétkor', datetime(2020, 12, 18, 7), datetime(2020, 12, 18, 7, 59, 59)),
        ('2021 január 5', datetime(2021, 1, 5), datetime(2021, 1, 5, 23, 59, 59)),
        ('2021 január 5 reggel 7', datetime(2021, 1, 5, 7), datetime(2021, 1, 5, 7, 59, 59)),
        ('január 5 reggel 7', datetime(2020, 1, 5, 7), datetime(2020, 1, 5, 7, 59, 59)),
        ('január 5-én', datetime(2020, 1, 5), datetime(2020, 1, 5, 23, 59, 59))
    ]
    now = datetime(2020, 12, 18)
    de = DatetimeExtractor(now)

    for inp_txt, st, end in tf:
        parsed_date = de.parse_datetime(inp_txt)[0]

        assert parsed_date['start_date'] == st
        assert parsed_date['end_date'] == end


def test_extend_start_end():
    inp_1 = {'start_date': [], 'end_date': [Hour(1, '')]}
    assert extend_start_end(inp_1) == inp_1

    inp_2 = {'start_date': [Month(1, ''), Hour(1, '')], 'end_date': []}
    assert extend_start_end(inp_2) == {'start_date': [Month(1, ''), Hour(1, '')],
                                       'end_date': [Month(1, ''), Hour(1, '')]}
