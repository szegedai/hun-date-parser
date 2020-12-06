import re
from collections import namedtuple
from typing import Tuple, Union, List, Dict
from datetime import datetime, timedelta

from .patterns import (R_ISO_DATE, R_NAMED_MONTH, R_TODAY, R_TOMORROW, R_NTOMORROW, R_YESTERDAY, R_NYESTERDAY,
                       R_NDAYS_FROM_NOW, R_WEEKDAY)
from .utils import remove_accent

Year = namedtuple('Year', ['x'])
Month = namedtuple('Month', ['x'])
Day = namedtuple('Day', ['x'])
Hour = namedtuple('Hour', ['x'])
Minute = namedtuple('Minute', ['x'])
Second = namedtuple('Second', ['x'])


def match_iso_date(s: str) -> Dict:
    """
    Match ISO date-like format.
    :param s: textual input
    :return: tuple of date parts
    """
    match = re.findall(R_ISO_DATE, s)

    res = []
    if match:
        for group in match:
            group = [int(m.lstrip('0')) for m in group if m]

            if len(group) == 1:
                res.append({'match': group, 'date_parts': [Year(group[0])]})
            elif len(group) == 2:
                res.append({'match': group, 'date_parts': [Year(group[0]), Month(group[1])]})
            elif len(group) == 3:
                res.append({'match': group, 'date_parts': [Year(group[0]), Month(group[1]), Day(group[2])]})

    return res


def match_named_month(s: str) -> Dict:
    """
    Match named month and day
    :param s: textual input
    :return: tuple of date parts
    """
    groups = re.findall(R_NAMED_MONTH, s)
    months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'szep', 'okt', 'nov', 'dec']

    res = []
    groups = [(m, d.lstrip('0')) if d else [m] for m, d in groups]
    for group in groups:
        group_res = {'match': group, 'date_parts': []}
        for i, month in enumerate(months):
            if month in remove_accent(group[0]):
                group_res['date_parts'].append(Month(i + 1))
                break

        if len(group) == 2:
            group_res['date_parts'].append(Day(int(group[1])))

        res.append(group_res)

    return res


def match_relative_day(s: str, now: datetime) -> Dict:
    groups = [*re.findall(R_TODAY, s),
              *re.findall(R_TOMORROW, s),
              *re.findall(R_NTOMORROW, s),
              *re.findall(R_YESTERDAY, s),
              *re.findall(R_NYESTERDAY, s)]

    res = []
    for group in groups:

        if type(group) != str:
            group = [m for m in group if m][0]

        if 'ma' in group or 'má' in group:
            res.append({'match': group, 'date_parts': [Year(now.year), Month(now.month), Day(now.day)]})
        elif 'holnapu' in group:
            tom2 = now + timedelta(days=2)
            res.append({'match': group, 'date_parts': [Year(tom2.year), Month(tom2.month), Day(tom2.day)]})
        elif 'holnap' in group:
            tom = now + timedelta(days=1)
            res.append({'match': group, 'date_parts': [Year(tom.year), Month(tom.month), Day(tom.day)]})
        elif 'tegnapel' in group:
            yes2 = now - timedelta(days=2)
            res.append({'match': group, 'date_parts': [Year(yes2.year), Month(yes2.month), Day(yes2.day)]})
        elif 'tegnap' in group:
            yes = now - timedelta(days=1)
            res.append({'match': group, 'date_parts': [Year(yes.year), Month(yes.month), Day(yes.day)]})

    return res


def match_relative_day(s: str, now: datetime) -> Dict:
    groups = re.findall(R_WEEKDAY, s)

    res = []
    for group in groups:

        if type(group) != str:
            group = [m for m in group if m][0]

        if 'hetfo' in remove_accent(group):
            res.append({'match': group, 'date_parts': [Year(now.year), Month(now.month), Day(now.day)]})