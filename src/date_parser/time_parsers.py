import re

from typing import Dict

from .patterns import R_AT, R_DIGI, R_HWORDS, R_HOUR_MIN
from .utils import remove_accent, word_to_num, Year, Month, Week, Day, Hour, Minute, Second, Interval, Daypart


def match_digi_clock(s: str) -> Dict:
    """
    Match digi clock format.
    :param s: textual input
    :return: tuple of date parts
    """
    match = re.findall(R_DIGI, s)

    res = []
    for group in match:
        group = [int(m.lstrip('0')) for m in group if m.lstrip('0')]

        if len(group) == 2:
            h, m = group
            res.append({'match': group, 'date_parts': [Hour(h), Minute(m)]})
        elif len(group) == 1:
            res.append({'match': group, 'date_parts': [Hour(group[0])]})

    return res


def match_time_words(s: str) -> Dict:
    """
    :param s: textual input
    :return: tuple of date parts
    """
    group = re.findall(R_HOUR_MIN, s)
    group = [m for m in group if ''.join(m)][0]

    print(group)

    res = []
    am = True
    date_parts = []
    daypart, hour, minute = group

    if daypart and hour:
        if 'reggel' in daypart or 'delelott' in remove_accent(daypart) or 'hajnal' in daypart:
            am = True
        elif 'delutan' in remove_accent(daypart) or 'este' in daypart or 'ejjel' in remove_accent(daypart):
            am = False

    if hour:
        hour_num = word_to_num(hour)

        if hour_num == -1:
            return []
        else:
            if hour_num < 12 and not am:
                hour_num += 12

            date_parts.append(Hour(hour_num))

        if minute:
            minute_num = word_to_num(minute)
            if minute_num != -1:
                date_parts.append(Minute(minute_num))

        res.append({'match': group, 'date_parts': date_parts})

    elif daypart:
        if 'hajnal' in daypart:
            res.append({'match': group, 'date_parts': [Daypart(0)]})
        elif 'reggel' in daypart:
            res.append({'match': group, 'date_parts': [Daypart(1)]})
        elif 'delelott' in remove_accent(daypart):
            res.append({'match': group, 'date_parts': [Daypart(2)]})
        elif 'delutan' in remove_accent(daypart):
            res.append({'match': group, 'date_parts': [Daypart(3)]})
        elif 'este' in daypart:
            res.append({'match': group, 'date_parts': [Daypart(4)]})
        elif 'ejjel' in remove_accent(daypart):
            res.append({'match': group, 'date_parts': [Daypart(5)]})

    return res