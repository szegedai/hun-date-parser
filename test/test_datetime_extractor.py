from datetime import datetime

from hun_date_parser.date_parser.datetime_extractor import DatetimeExtractor, assamble_datetime


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
