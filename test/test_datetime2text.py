from datetime import time, datetime

from hun_date_parser.date_textualizer.time2text import time2lifelike, time2digi, time2relitivetexttime, \
    time2absolutetexttime
from hun_date_parser.date_textualizer.date2text import date2text


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


def test_time2relitivetexttime():
    tf = [(time(22, 50), 2, 'este tíz óra ötven perc'),
          (time(22, 50), 3, 'este tíz óra ötven perc nulla másodperc')]

    for inp, res, out in tf:
        assert time2relitivetexttime(inp, resolution=res) == out


def test_time2absolutetexttime():
    tf = [(time(22, 50), 2, 'huszonkettő óra ötven perc'),
          (time(22, 50), 3, 'huszonkettő óra ötven perc nulla másodperc')]

    for inp, res, out in tf:
        assert time2absolutetexttime(inp, resolution=res) == out


def test_time2digi():
    tf = [(time(22, 50), 2, '22:50'),
          (time(22, 50), 3, '22:50:00')]

    for inp, res, out in tf:
        assert time2digi(inp, resolution=res) == out


def test_date2text():
    now = datetime(2020, 12, 27)
    tf = [(datetime(2020, 12, 27), 'ma'),
          (datetime(2020, 12, 28), 'holnap'),
          (datetime(2020, 12, 21), 'ezen a héten hétfőn'),
          (datetime(2020, 12, 20), 'múlt héten vasárnap'),
          (datetime(2020, 12, 19), 'múlt héten szombaton'),
          (datetime(2020, 12, 29), 'jövő hét kedden'),
          (datetime(2020, 12, 13), 'két hete vasárnap')]

    for inp, out in tf:
        assert date2text(inp, now=now) == out
