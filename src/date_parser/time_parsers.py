import re

from typing import Dict

from .patterns import R_AT, R_DIGI, R_HWORDS
from .utils import remove_accent, Year, Month, Week, Day, Hour, Minute


def match_digi_clock(s: str) -> Dict:
    """
    Match digi clock format.
    :param s: textual input
    :return: tuple of date parts
    """
    match = re.findall(R_DIGI, s)

    res = []
    for group in match:
        group = [int(m.lstrip('0')) for m in group if m]
        h, m = group

        res.append({'match': group, 'date_parts': [Hour(h), Minute(m)]})

    return res