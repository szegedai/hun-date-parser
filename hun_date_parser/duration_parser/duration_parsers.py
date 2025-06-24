from typing import TypedDict, Optional, Sequence, Union, List
import re
from hun_date_parser.utils import (DateTimePartConatiner, remove_accent, word_to_num,
                                   Minute, Hour, Day, Week, Month, Year)
from hun_date_parser.date_parser.patterns import (R_HOUR_MIN_D, R_HOUR_HOUR_D,
                                                  R_HOUR_D, R_SPECIAL_HOUR_D)
from enum import Enum


class DurationUnit(str, Enum):
    """Enum for duration unit preferences"""
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    YEARS = "years"


class DateParts(TypedDict):
    match: str
    date_parts: Sequence[DateTimePartConatiner]
    preferred_unit: Optional[DurationUnit]


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


def duration_parser(s: str, return_preferred_unit: bool = False) -> DateParts:
    s_clean = s.strip().lower()
    s_no_accent = remove_accent(s_clean)

    preferred_unit: Optional[DurationUnit] = None
    res_date_parts: List[DateTimePartConatiner] = []

    # Year patterns
    year_pattern = (r'\b(\d+|egy|kett[oöő]|két|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|kilenc|'
                    r't[ií]z|teljes)?\s*[eé]v(ese?[eé]?t?|re)\b')
    if re.search(year_pattern, s_no_accent):
        year_match_pattern = (r'(\d+|egy|kett[oöő]|két|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|'
                              r'kilenc|t[ií]z|teljes)\s*[eé]v(ese?[eé]?t?|re)')
        num_match = re.search(year_match_pattern, s_no_accent)
        if num_match:
            num_str = num_match.group(1)
            if num_str == 'teljes':
                num_years = 1
            else:
                num_years = word_to_num(num_str) if num_str.isalpha() else int(num_str)
        else:
            num_years = 1

        if return_preferred_unit:
            res_date_parts = [Year(num_years, "duration_parser")]
            preferred_unit = DurationUnit.YEARS
        else:
            res_date_parts = [Minute(num_years * 365 * 24 * 60, "duration_parser")]

    # Week patterns
    elif re.search(r'\b(\d+|egy|kett[oöő]|k[eé]t|k[eé]thetes|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|'
                   r'nyolc|kilenc|t[ií]z)\s*h[eé]t(ese?[eé]?t?|re)\b', s_no_accent):
        week_match_pattern = (r'(\d+|egy|kett[oöő]|k[eé]t|k[eé]thetes|h[aá]rom|n[eé]gy|[öo]t|hat|'
                              r'h[eé]t|nyolc|kilenc|t[ií]z)\s*h[eé]t(ese?[eé]?t?|re)')
        num_match = re.search(week_match_pattern, s_no_accent)
        if num_match:
            num_str = num_match.group(1)
            num_weeks = word_to_num(num_str) if num_str.isalpha() else int(num_str)
        else:
            num_weeks = 1

        if return_preferred_unit:
            res_date_parts = [Week(num_weeks, "duration_parser")]
            preferred_unit = DurationUnit.WEEKS
        else:
            res_date_parts = [Minute(num_weeks * 7 * 24 * 60, "duration_parser")]

    # Day patterns
    elif re.search(r'\b(\d+|egy|kett[oöő]|két|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|kilenc|'
                   r't[ií]z|harminc|\d{2,3})\s*nap(osa?[aá]?t?|ra)\b', s_no_accent):
        day_match_pattern = (r'(\d+|egy|kett[oöő]|két|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|'
                             r'kilenc|t[ií]z|harminc|\d{2,3})\s*nap(osa?[aá]?t?|ra)')
        num_match = re.search(day_match_pattern, s_no_accent)
        if num_match:
            num_str = num_match.group(1)
            num_days = word_to_num(num_str) if num_str.isalpha() else int(num_str)
            if return_preferred_unit:
                res_date_parts = [Day(num_days, "duration_parser")]
                preferred_unit = DurationUnit.DAYS
            else:
                res_date_parts = [Minute(num_days * 24 * 60, "duration_parser")]

    # Hour patterns
    elif re.search(r'\b(\d+|egy|kett[oöő]|két|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|kilenc|'
                   r't[ií]z|\d{2})\s*[oó]r[aá](sa?[aá]?t?|ra)\b', s_no_accent):
        hour_match_pattern = (r'(\d+|egy|kett[oöő]|két|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|'
                              r'kilenc|t[ií]z|\d{2})\s*[oó]r[aá](sa?[aá]?t?|ra)')
        num_match = re.search(hour_match_pattern, s_no_accent)
        if num_match:
            num_str = num_match.group(1)
            num_hours = word_to_num(num_str) if num_str.isalpha() else int(num_str)
            # Reject unrealistic hour values (like 100)
            if num_hours > 50:
                res_date_parts = []
            elif return_preferred_unit:
                res_date_parts = [Hour(num_hours, "duration_parser")]
                preferred_unit = DurationUnit.HOURS
            else:
                res_date_parts = [Minute(num_hours * 60, "duration_parser")]

    # Fallback to original logic for existing patterns
    else:
        res_mins = 0
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

        if res_mins > 0:
            if return_preferred_unit and res_mins >= 60 and res_mins % 60 == 0:
                # Prefer hours for whole hour durations
                res_date_parts = [Hour(res_mins // 60, "duration_parser")]
                preferred_unit = DurationUnit.HOURS
            else:
                res_date_parts = [Minute(res_mins, "duration_parser")]
                preferred_unit = DurationUnit.MINUTES

    result: DateParts = {
        "match": s,
        "date_parts": res_date_parts,
        "preferred_unit": preferred_unit if return_preferred_unit else None
    }

    return result


def parse_duration(s: str, return_preferred_unit: bool = False) -> Union[Optional[int], Optional[dict]]:
    """
    Returns the duration found in the input string.
    :param s: Input string containing the duration information.
    :param return_preferred_unit: If True, returns a dict with value, unit, and preferred_unit.
                                 If False, returns minutes as int.
    :return: The duration in minutes as an integer (default), or a dict with duration info
             if return_preferred_unit=True. Returns None if no valid duration is found.
    """
    results = duration_parser(s, return_preferred_unit=return_preferred_unit)

    if not results["date_parts"]:
        return None

    if return_preferred_unit:
        date_part = results["date_parts"][0]
        preferred_unit = results.get("preferred_unit", DurationUnit.MINUTES)

        return {
            "value": date_part.value,
            "unit": type(date_part).__name__.lower(),
            "preferred_unit": preferred_unit.value if preferred_unit else DurationUnit.MINUTES.value,
            "minutes": _convert_to_minutes(date_part)
        }
    else:
        # Return minutes for backward compatibility
        return _convert_to_minutes(results["date_parts"][0])


def _convert_to_minutes(date_part: DateTimePartConatiner) -> int:
    """
    Helper function to convert any date part to minutes.
    """
    if date_part.value is None:
        return 0
    if isinstance(date_part, Minute):
        return date_part.value
    elif isinstance(date_part, Hour):
        return date_part.value * 60
    elif isinstance(date_part, Day):
        return date_part.value * 24 * 60
    elif isinstance(date_part, Week):
        return date_part.value * 7 * 24 * 60
    elif isinstance(date_part, Month):
        return date_part.value * 30 * 24 * 60  # Approximate
    elif isinstance(date_part, Year):
        return date_part.value * 365 * 24 * 60  # Approximate
    else:
        return 0
