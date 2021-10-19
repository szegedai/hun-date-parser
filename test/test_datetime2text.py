import pytest
from datetime import time, datetime

from hun_date_parser.date_textualizer.time2text import time2lifelike, time2digi, time2relitivetexttime, \
    time2absolutetexttime
from hun_date_parser.date_textualizer.date2text import date2text

tf_time2lifelike = [(time(22, 50), 'éjjel háromnegyed 11 után 5 perccel'),
                    (time(23, 44), 'éjjel háromnegyed 12 előtt 1 perccel'),
                    (time(8, 0), 'reggel 8 óra'),
                    (time(0), 'éjjel 12 óra'),
                    (time(10, 59), 'délelőtt 11 óra előtt 1 perccel'),
                    (time(4, 4), 'hajnal 4 óra után 4 perccel'),
                    (time(2, 16), 'éjjel negyed 3 után 1 perccel'),
                    (time(12), '12 óra'),
                    (time(11, 45), 'háromnegyed 12')]

tf_time2lifelike_res = [(time(22, 50), 2, 'éjjel háromnegyed 11 után 5 perccel'),
                        (time(22, 50), 1, 'este 10 óra'),
                        (time(11, 59, 59), 1, 'délelőtt 11 óra')]

tf_relitivetexttime = [(time(22, 50), 1, 'este tíz óra'),
                       (time(22, 50), 2, 'este tíz óra ötven perc'),
                       (time(22, 50), 3, 'este tíz óra ötven perc nulla másodperc')]

tf_absolutetexttime = [(time(22, 50), 1, 'huszonkettő óra'),
                       (time(22, 50), 2, 'huszonkettő óra ötven perc'),
                       (time(22, 50), 3, 'huszonkettő óra ötven perc nulla másodperc')]

tf_digi = [(time(22, 50), 2, '22:50'),
           (time(22, 50), 3, '22:50:00')]

tf_date = [(datetime(2020, 12, 27), 'ma'),
           (datetime(2020, 12, 28), 'holnap'),
           (datetime(2020, 12, 21), 'ezen a héten hétfőn'),
           (datetime(2020, 12, 20), 'múlt héten vasárnap'),
           (datetime(2020, 12, 19), 'múlt héten szombaton'),
           (datetime(2020, 12, 29), 'jövő hét kedden'),
           (datetime(2020, 12, 13), 'két hete vasárnap')]


@pytest.mark.parametrize("inp,out", tf_time2lifelike)
def test_time2lifelike(inp, out):
    assert time2lifelike(inp) == out


@pytest.mark.parametrize("inp,res,out", tf_time2lifelike_res)
def test_time2lifelike_res(inp, res, out):
    assert time2lifelike(inp, res) == out


@pytest.mark.parametrize("inp,res,out", tf_relitivetexttime)
def test_time2relitivetexttime(inp, res, out):
    assert time2relitivetexttime(inp, resolution=res) == out


@pytest.mark.parametrize("inp,res,out", tf_absolutetexttime)
def test_time2absolutetexttime(inp, res, out):
    assert time2absolutetexttime(inp, resolution=res) == out


@pytest.mark.parametrize("inp,res,out", tf_digi)
def test_time2digi(inp, res, out):
    assert time2digi(inp, resolution=res) == out


@pytest.mark.parametrize("inp,out", tf_date)
def test_date2text(inp, out):
    now = datetime(2020, 12, 27)
    assert date2text(inp, now=now) == out
