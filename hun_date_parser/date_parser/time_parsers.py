import re

from typing import Dict, List, Any

from .patterns import R_DIGI, R_HOUR_MIN, R_HOUR_MIN_REV
from hun_date_parser.utils import remove_accent, word_to_num, Hour, Minute, Daypart

NAN = -1


def match_digi_clock(s: str) -> List[Dict[str, Any]]:
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
            res.append({'match': group, 'date_parts': [Hour(h, 'digi_clock'), Minute(m, 'digi_clock')]})
        elif len(group) == 1:
            res.append({'match': group, 'date_parts': [Hour(group[0], 'digi_clock')]})

    return res


def match_time_words(s: str) -> List[Dict[str, Any]]:
    """
    :param s: textual input
    :return: tuple of date parts
    """
    group = re.findall(R_HOUR_MIN, s)
    group = [m for m in group if ''.join(m)]

    group_rev = re.findall(R_HOUR_MIN_REV, s)
    group_rev = [m for m in group_rev if ''.join(m)]

    if not (group or group_rev):
        return []
    elif group and not group_rev:
        daypart, hour_modifier, hour, minute = group[0]
    elif not group and group_rev:
        minute, daypart, hour_modifier, hour, is_before = group_rev[0]
        minute += (' ' + is_before)
    elif group_rev[0].count('') < group[0].count(''):
        minute, daypart, hour_modifier, hour, is_before = group_rev[0]
        minute += (' ' + is_before)
    else:
        daypart, hour_modifier, hour, minute = group[0]

    # Only numbers can match dates as well, this is an attempt to remove false matches
    hour_index = s.index(hour)
    before_hour = s[:hour_index].split()
    months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'szep', 'okt', 'nov', 'dec']
    for month in months:
        if month in remove_accent(before_hour[-1]):
            return []

    res = []
    am = True
    date_parts = []

    if daypart and hour:
        if 'reggel' in daypart or 'delelott' in remove_accent(daypart) or 'hajnal' in daypart:
            am = True
        elif 'delutan' in remove_accent(daypart) or 'este' in daypart or 'ejjel' in remove_accent(daypart):
            am = False

    if hour:
        # this is made redundant by the change in the patterns
        non_hours = ['ev', 'perc']
        for nh in non_hours:
            if f' {nh}' in remove_accent(hour) or remove_accent(hour).startswith(nh):
                return []

        hour_num = word_to_num(hour)
        minute_num = word_to_num(minute)

        if hour_modifier:
            if 'haromnegyed' in remove_accent(hour_modifier):
                hour_num = hour_num-1 if hour_num-1 >= 0 else 23
                minute_num = 45
            elif 'fel' in remove_accent(hour_modifier):
                hour_num = hour_num-1 if hour_num-1 >= 0 else 23
                minute_num = 30
            elif 'negyed' in remove_accent(hour_modifier):
                hour_num = hour_num-1 if hour_num-1 >= 0 else 23
                minute_num = 15

        if hour_num == NAN:
            return []
        else:
            if hour_num < 12 and not am:
                hour_num += 12

        if minute or hour_modifier:
            # this is made redundant by the change in the patterns
            non_minutes = ['ev', 'ora']
            for nm in non_minutes:
                if f' {nm}' in remove_accent(minute) or remove_accent(minute).startswith(nm):
                    return []

            if 'elott' in remove_accent(minute) and not hour_modifier:
                hour_num -= (minute_num // 60) + 1
                hour_num = hour_num if hour_num >= 0 else 23
                date_parts.extend([Hour(hour_num, 'time_words'), Minute(60-(minute_num % 60), 'time_words')])
            elif 'elott' in remove_accent(minute) and hour_modifier:
                n_minutes_before = word_to_num(minute)
                if n_minutes_before != NAN:
                    minute_num -= n_minutes_before
                if minute_num < 0:
                    hour_num += (minute_num // 60)
                    hour_num = hour_num if hour_num >= 0 else 23
                    minute_num = minute_num % 60
                date_parts.extend([Hour(hour_num, 'time_words'), Minute(minute_num, 'time_words')])
            elif hour_modifier:
                n_minutes_after = word_to_num(minute)
                if n_minutes_after != NAN:
                    minute_num += n_minutes_after
                if minute_num > 59:
                    hour_num += (minute_num // 60)
                    hour_num = hour_num if hour_num <= 23 else 0
                    minute_num = minute_num % 60
                date_parts.extend([Hour(hour_num, 'time_words'), Minute(minute_num, 'time_words')])
            else:
                date_parts.extend([Hour(hour_num, 'time_words'), Minute(minute_num, 'time_words')])

        else:
            date_parts.append(Hour(hour_num, 'time_words'))

        res.append({'match': group, 'date_parts': date_parts})

    elif daypart:
        if 'hajnal' in daypart:
            res.append({'match': group, 'date_parts': [Daypart(0, 'time_words')]})
        elif 'reggel' in daypart:
            res.append({'match': group, 'date_parts': [Daypart(1, 'time_words')]})
        elif 'delelott' in remove_accent(daypart):
            res.append({'match': group, 'date_parts': [Daypart(2, 'time_words')]})
        elif 'delutan' in remove_accent(daypart):
            res.append({'match': group, 'date_parts': [Daypart(3, 'time_words')]})
        elif 'este' in daypart:
            res.append({'match': group, 'date_parts': [Daypart(4, 'time_words')]})
        elif 'ejjel' in remove_accent(daypart):
            res.append({'match': group, 'date_parts': [Daypart(5, 'time_words')]})

    return res
