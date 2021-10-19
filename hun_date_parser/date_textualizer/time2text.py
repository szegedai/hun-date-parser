from datetime import time

from hun_date_parser.utils import num_to_word

hours_word = {
    0: 'nulla',
    1: 'hajnali egy',
    2: 'hajnali kettő',
    3: 'hajnali három',
    4: 'hajnali négy',
    5: 'hajnali öt',
    6: 'reggel hat',
    7: 'reggel hét',
    8: 'reggel nyolc',
    9: 'reggel kilenc',
    10: 'délelőtt tíz',
    11: 'délelőtt tizenegy',
    12: 'tizenkét',
    13: 'délután egy',
    14: 'délután kettő',
    15: 'délután három',
    16: 'délután négy',
    17: 'délután öt',
    18: 'este hat',
    19: 'este hét',
    20: 'este nyolc',
    21: 'este kilenc',
    22: 'este tíz',
    23: 'este tizenegy',
}

dayparts = {
    0: 'éjjel',
    3: 'hajnal',
    6: 'reggel',
    10: 'délelőtt',
    12: 'délután',
    18: 'este',
    22: 'éjjel',
    24: 'éjjel'
}


def get_daypart(h: int):
    if h == 12:
        return ''
    for i, (k, v) in enumerate(dayparts.items()):
        if k <= h <= list(dayparts)[i+1]:
            return v


def time2relitivetexttime(t: time, resolution: int):
    assert 1 <= resolution <= 3

    if resolution >= 1:
        hour = t.hour
        hour_rep = hours_word[hour]

    if resolution >= 2:
        minute = t.minute
        minute_res = num_to_word(minute)

    if resolution >= 3:
        second = t.second
        second_res = num_to_word(second)

    if resolution == 1:
        if hour == 0:
            return 'éjfél'
        elif hour == 12:
            return 'dél'
        else:
            return f"{hour_rep} óra"
    elif resolution == 2:
        return f"{hour_rep} óra {minute_res} perc"
    elif resolution == 3:
        return f"{hour_rep} óra {minute_res} perc {second_res} másodperc"


def time2absolutetexttime(t: time, resolution: int):
    assert 1 <= resolution <= 3

    if resolution >= 1:
        hour = t.hour
        hour_rep = num_to_word(hour)

    if resolution >= 2:
        minute = t.minute
        minute_res = num_to_word(minute)

    if resolution >= 3:
        second = t.second
        second_res = num_to_word(second)

    if resolution == 1:
        return f"{hour_rep} óra"
    elif resolution == 2:
        return f"{hour_rep} óra {minute_res} perc"
    elif resolution == 3:
        return f"{hour_rep} óra {minute_res} perc {second_res} másodperc"


def time2digi(t: time, resolution: int):
    assert 1 <= resolution <= 3

    if resolution == 1:
        return f'{t.hour}'
    if resolution == 2:
        return f'{str(t.hour).zfill(2)}:{str(t.minute).zfill(2)}'
    if resolution == 3:
        return f'{str(t.hour).zfill(2)}:{str(t.minute).zfill(2)}:{str(t.second).zfill(2)}'


def time2lifelike(t: time, resolution: int = 2):

    if resolution == 1:
        t = time(t.hour, 0)

    def get_h_rep(h):
        if h % 12 != 0:
            return h % 12
        else:
            return 12

    h, m = t.hour, t.minute

    h_ = h + 1 if h <= 23 else 0

    if m == 0:
        return f'{get_daypart(h)} {get_h_rep(h)} óra'.lstrip()
    elif 0 < m < 10:
        return f'{get_daypart(h)} {get_h_rep(h)} óra után {m} perccel'.lstrip()
    elif 10 <= m < 15:
        return f'{get_daypart(h_)} negyed {get_h_rep(h_)} előtt {15 - m} perccel'.lstrip()
    elif m == 15:
        return f'{get_daypart(h_)} negyed {get_h_rep(h_)}'.lstrip()
    elif 15 < m <= 20:
        return f'{get_daypart(h_)} negyed {get_h_rep(h_)} után {m - 15} perccel'.lstrip()
    elif 20 < m < 30:
        return f'{get_daypart(h_)} fél {get_h_rep(h_)} előtt {30 - m} perccel'.lstrip()
    elif m == 30:
        return f'{get_daypart(h_)} fél {get_h_rep(h_)}'.lstrip()
    elif 30 < m <= 40:
        return f'{get_daypart(h_)} fél {get_h_rep(h_)} után {m - 30} perccel'.lstrip()
    elif 40 < m < 45:
        return f'{get_daypart(h_)} háromnegyed {get_h_rep(h_)} előtt {45 - m} perccel'.lstrip()
    elif m == 45:
        return f'{get_daypart(h_)} háromnegyed {get_h_rep(h_)}'.lstrip()
    elif 45 < m <= 50:
        return f'{get_daypart(h_)} háromnegyed {get_h_rep(h_)} után {m - 45} perccel'.lstrip()
    elif 50 < m:
        return f'{get_daypart(h_)} {get_h_rep(h_)} óra előtt {60 - m} perccel'.lstrip()
    else:
        return ''
