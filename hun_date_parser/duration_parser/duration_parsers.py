from typing import TypedDict, Optional, Sequence
import re
from hun_date_parser.utils import DateTimePartConatiner, remove_accent, word_to_num, Minute
from hun_date_parser.date_parser.patterns import R_HOUR_MIN_D, R_HOUR_HOUR_D, R_HOUR_D, R_SPECIAL_HOUR_D


class DateParts(TypedDict):
    match: str
    date_parts: Sequence[DateTimePartConatiner]


def convert_hour_to_minutes(hour_str: Optional[str]) -> int:
    """Converts an hour string to minutes, handling special cases."""
    if hour_str is None:
        return 0
    if ",5" in hour_str:
        hour_num = word_to_num(hour_str.replace(",5", ""))
        if hour_num != -1:
            return int((hour_num + 0.5) * 60)
    else:
        hour_num = word_to_num(hour_str)
        if hour_num != -1:
            return hour_num * 60
    return 0


def convert_quarter_hour(hour_str: Optional[str]) -> int:
    """Converts a quarter hour string to minutes."""
    if hour_str is None:
        return 0
    hour_str_no_accent = remove_accent(hour_str)
    if "haromnegyed" in hour_str_no_accent:
        return 45
    if "negyed" in hour_str_no_accent and "haromnegyed" not in hour_str_no_accent:
        return 15
    if "fel" in hour_str_no_accent and "masfel" not in hour_str_no_accent:
        return 30
    if "masfel" in hour_str_no_accent:
        return 90
    return 0


def duration_parser(s: str) -> DateParts:
    # First handle '3 negyedóra' pattern
    if re.search(r'3\s+negyed', s):
        res_mins = 45
    # Handle all háromnegyed forms
    elif re.search(r'h[aá]romnegyed\s*[oó]r[aá](?:[tr][aá])?', s):
        res_mins = 45
    else:
        match = re.match(R_HOUR_MIN_D, s)
        if match:
            hour_w, min_w = match.groups()
            mins_1 = convert_hour_to_minutes(hour_w)
            mins_2 = word_to_num(min_w)
            res_mins = mins_1 + mins_2
        else:
            match = re.match(R_HOUR_D, s)
            if match:
                hour_w = match.groups()[0]
                res_mins = convert_hour_to_minutes(hour_w)
            else:
                match = re.match(R_HOUR_HOUR_D, s)
                if match:
                    hour_w, hour_w_2 = match.groups()
                    mins_1 = convert_hour_to_minutes(hour_w)
                    mins_2 = convert_quarter_hour(hour_w_2)
                    res_mins = mins_1 + mins_2
                else:
                    match = re.match(R_SPECIAL_HOUR_D, s)
                    if match:
                        special_hour = match.groups()[0]
                        res_mins = convert_quarter_hour(special_hour)
                    else:
                        res_mins = 0

    res_date_parts = [Minute(res_mins, "duration_parser")] if res_mins > 0 else []

    return {
        "match": s,
        "date_parts": res_date_parts
    }


def parse_duration(s: str) -> Optional[int]:
    """
    Returns the duration in minutes found in the input string.
    :param s: Input string containing the duration information.
    :return: The duration in minutes as an integer, or None if no valid duration is found.
    """
    results = duration_parser(s)
    return results["date_parts"][0].value if results["date_parts"] else None
