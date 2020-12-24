from datetime import time

from src.utils import num_to_word

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
