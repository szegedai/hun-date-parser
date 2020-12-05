import re
from collections import namedtuple
from typing import Tuple, Union, List, Dict

from .patterns import R_ISO_DATE, R_NAMED_MONTH
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
