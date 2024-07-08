from typing import List, TypedDict

import re

from hun_date_parser.utils import DateTimePartConatiner, remove_accent, word_to_num, Minute
from hun_date_parser.date_parser.patterns import R_HOUR_MIN_D, R_HOUR_HOUR_D, R_HOUR_D


class DateParts(TypedDict):
    match: str
    date_parts: List[DateTimePartConatiner]


def duration_parser(s: str) -> DateParts:

    hour_w, hour_w_2, min_w = None, None, None
    mins_1, mins_2, mins_3 = 0, 0, 0

    match = re.match(R_HOUR_MIN_D, s)
    if match:
        hour_w, min_w = match.groups()
    else:
        match = re.match(R_HOUR_D, s)
        if match:
            hour_w = match.groups()[0]
        else:
            match = re.match(R_HOUR_HOUR_D, s)
            if match:
                hour_w, hour_w_2 = match.groups()

    if hour_w:

        if ",5" in hour_w:
            hour_num = word_to_num(hour_w.replace(",5", ""))
            if hour_num != -1:
                hour_num = hour_num + 0.5
        else:
            hour_num = word_to_num(hour_w)

        if hour_num != -1:
            mins_1 = hour_num * 60

    if hour_w_2:
        if "haromnegyed" in remove_accent(hour_w_2):
            mins_2 = 45
        elif "negyed" in hour_w_2:
            mins_2 = 15
        elif "fel" in remove_accent(hour_w_2):
            mins_2 = 30

    if min_w:
        mins_3 = word_to_num(min_w)

    res_mins = mins_1 + mins_2 + mins_3
    if res_mins > 0:
        res_date_parts = [Minute(res_mins, "duration_parser")]
    else:
        res_date_parts = []

    results: DateParts = {
        "match": s,
        "date_parts": res_date_parts
    }

    return results
