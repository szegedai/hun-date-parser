from src.date_parser.utils import Year, Month, Week, Day, Daypart, Hour, Minute, Second
from src.date_parser.time_parsers import match_digi_clock, match_time_words


def test_match_relative_week():
    tf = [('kedden 8:45', [[Hour(8), Minute(45)]]),
          ('kedden 08:45', [[Hour(8), Minute(45)]]),
          ('ma este 18:12-kor', [[Hour(18), Minute(12)]])]

    for inp, exp in tf:
        out = match_digi_clock(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_time_words():
    tf = [('reggel nyolc előtt hat perccel', [[Hour(7), Minute(54)]]),
          ('reggel nyolc előtt nyolcvan perccel', [[Hour(6), Minute(40)]]),
          ('este 8 előtt 12 perccel', [[Hour(19), Minute(48)]]),
          ('nyolc óra nyolc perckor', [[Hour(8), Minute(8)]]),
          ('ma reggel hat óra', [[Hour(6)]]),
          ('ma reggel', [[Daypart(1)]]),
          ('ma délután háromkor', [[Hour(15)]]),
          ('ma délután három után negyvenhat perckor', [[Hour(15), Minute(46)]]),
          ('ma délután haemdknc után negyvenhat perckor', [[Daypart(3)]]),
          ('ma', []),
          ('ötvenöt perckor', []),
          ('húsz óra negyvenkilenc perckor', [[Hour(20), Minute(49)]]),
          ('20 óra negyvenkilenc perckor', [[Hour(20), Minute(49)]]),
          ('20 óra 49 perckor', [[Hour(20), Minute(49)]]),
          ('este 8-kor', [[Hour(20)]]),
          ('este háromnegyed 8-kor', [[Hour(19), Minute(45)]]),
          ('este negyed 8-kor', [[Hour(19), Minute(15)]]),
          ('háromnegyed nyolckor', [[Hour(7), Minute(45)]]),
          ('este negyed 8 előtt 6 perccel', [[Hour(19), Minute(9)]]),
          ('este háromnegyed 8 előtt két perccel', [[Hour(19), Minute(43)]]),
          ('este fél 8 előtt harminckilenc perccel', [[Hour(18), Minute(51)]]),
          ('este fél 8 előtt', [[Hour(19), Minute(30)]]),
          ('harminckilenc perccel este fél 8 előtt', [[Hour(18), Minute(51)]]),
          ('mondjuk két perccel 6 után', [[Hour(6), Minute(2)]]),
          ('mondjuk tíz perccel 8 óra előtt', [[Hour(7), Minute(50)]])]

    for inp, exp in tf:
        out = match_time_words(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp
