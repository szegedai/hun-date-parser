import re
from collections import namedtuple
from typing import Tuple, Union

from .patterns import R_ISO_DATE, R_NAMED_MONTH

Year = namedtuple('Year', ['x'])
Month = namedtuple('Month', ['x'])
Day = namedtuple('Day', ['x'])
Hour = namedtuple('Hour', ['x'])
Minute = namedtuple('Minute', ['x'])
Second = namedtuple('Second', ['x'])


def match_iso_date(s: str) -> Tuple[Union[Year, Month, Day]]:
    """
    Match ISO date-like format.
    :param s: textual input
    :return: tuple of date parts
    """
    match = re.match(R_ISO_DATE, s)

    res = []
    if match:
        groups = match.groups()
        groups = [int(m.lstrip('0')) for m in groups if m]

        if len(groups) == 1:
            res.append(Year(groups[0]))
        elif len(groups) == 2:
            res.append(Year(groups[0]), Month(groups[1]))
        elif len(groups) == 3:
            res.append(Year(groups[0]), Month(groups[1]), Day(groups[2]))

    return tuple(res)


def match_named_month(s: str) -> Tuple[Union[Month, Day]]:
    """
    Match named month and day
    :param s: textual input
    :return: tuple of date parts
    """
    match = re.match(R_NAMED_MONTH, s)
    months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'szep', 'okt', 'nov', 'dec']

    res = []
    if match:
        groups = match.groups()
        groups = [m.lstrip('0') for m in groups if m]

        if groups:
            for i, month in enumerate(months):
                if month in groups[0]:
                    res.append(Month(i + 1))

            if len(groups) == 2:
                res.append(Day(int(groups[1])))

    return tuple(res)
