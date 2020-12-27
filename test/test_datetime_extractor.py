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
         datetime(2020, 12, 19, 7, 43, 59))
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
