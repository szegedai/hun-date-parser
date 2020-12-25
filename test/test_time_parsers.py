from hun_date_parser.utils import Daypart, Hour, Minute
from hun_date_parser.date_parser.time_parsers import match_digi_clock, match_time_words


def test_match_digi_clock():
    fn = 'digi_clock'
    tf = [('kedden 8:45', [[Hour(8, fn), Minute(45, fn)]]),
          ('kedden 08:45', [[Hour(8, fn), Minute(45, fn)]]),
          ('ma este 18:12-kor', [[Hour(18, fn), Minute(12, fn)]])]

    for inp, exp in tf:
        out = match_digi_clock(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp


def test_match_time_words():
    fn = 'time_words'
    tf = [('reggel nyolc előtt hat perccel', [[Hour(7, fn), Minute(54, fn)]]),
          ('reggel nyolc előtt nyolcvan perccel', [[Hour(6, fn), Minute(40, fn)]]),
          ('este 8 előtt 12 perccel', [[Hour(19, fn), Minute(48, fn)]]),
          ('nyolc óra nyolc perckor', [[Hour(8, fn), Minute(8, fn)]]),
          ('ma reggel hat óra', [[Hour(6, fn)]]),
          ('ma reggel', [[Daypart(1, fn)]]),
          ('ma délután háromkor', [[Hour(15, fn)]]),
          ('ma délután három után negyvenhat perckor', [[Hour(15, fn), Minute(46, fn)]]),
          ('ma délután haemdknc után negyvenhat perckor', [[Daypart(3, fn)]]),
          ('ma', []),
          ('ötvenöt perckor', []),
          ('húsz óra negyvenkilenc perckor', [[Hour(20, fn), Minute(49, fn)]]),
          ('20 óra negyvenkilenc perckor', [[Hour(20, fn), Minute(49, fn)]]),
          ('20 óra 49 perckor', [[Hour(20, fn), Minute(49, fn)]]),
          ('este 8-kor', [[Hour(20, fn)]]),
          ('este háromnegyed 8-kor', [[Hour(19, fn), Minute(45, fn)]]),
          ('este negyed 8-kor', [[Hour(19, fn), Minute(15, fn)]]),
          ('háromnegyed nyolckor', [[Hour(7, fn), Minute(45, fn)]]),
          ('este negyed 8 előtt 6 perccel', [[Hour(19, fn), Minute(9, fn)]]),
          ('este háromnegyed 8 előtt két perccel', [[Hour(19, fn), Minute(43, fn)]]),
          ('este fél 8 előtt harminckilenc perccel', [[Hour(18, fn), Minute(51, fn)]]),
          ('este fél 8 előtt', [[Hour(19, fn), Minute(30, fn)]]),
          ('harminckilenc perccel este fél 8 előtt', [[Hour(18, fn), Minute(51, fn)]]),
          ('mondjuk két perccel 6 után', [[Hour(6, fn), Minute(2, fn)]]),
          ('mondjuk tíz perccel 8 óra előtt', [[Hour(7, fn), Minute(50, fn)]]),
          ('délután fél négy után hat perccel', [[Hour(15, fn), Minute(36, fn)]]),
          ('6 óra után 3 perccel', [[Hour(6, fn), Minute(3, fn)]]),
          ('ezen a héten', []),
          ('2020 december', []),
          ('kb húsz év múlva', []),
          ('kb húsz évvel ezelőtt', [])]

    for inp, exp in tf:
        out = match_time_words(inp)
        date_parts = []
        for e in out:
            date_parts.append(e['date_parts'])
        assert date_parts == exp
