from enum import Enum
import re
from typing import Optional
from hun_date_parser.utils import remove_accent


class Frequency(str, Enum):
    """Enum for frequency values"""
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    FORTNIGHTLY = "FORTNIGHTLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    EVERY_HALF_YEAR = "EVERY_HALF_YEAR"
    YEARLY = "YEARLY"


def parse_frequency(s: str) -> Optional[dict]:
    """
    Returns the frequency value found in the input string along with match start and end indices.

    :param s: Input string containing the frequency information in Hungarian.
    :return: Dictionary with frequency value, start and end indices, or None if no valid frequency is found.
    """
    s = s.lower().strip()
    s_no_accent = remove_accent(s)

    frequency_map = {
        r'\bnap(onta|i|it|onkent)\b': Frequency.DAILY,
        r'\bminden nap\b': Frequency.DAILY,
        r'\bhet(ente|i|it|enkent)\b': Frequency.WEEKLY,
        r'\bminden het(en|eben)\b': Frequency.WEEKLY,
        r'\bheti rendszeresseg(gel)?\b': Frequency.WEEKLY,
        r'\bkethet(ente|i|it|enkent)\b': Frequency.FORTNIGHTLY,
        r'\bhav(onta|i|it|onkent)\b': Frequency.MONTHLY,
        r'\bhavi rendszeresseg(gel)?\b': Frequency.MONTHLY,
        r'\bnegyed(ev|eve)nte\b': Frequency.QUARTERLY,
        r'\bharomhav(onta|i)\b': Frequency.QUARTERLY,
        r'\bminden negyed(ev|eve)ben\b': Frequency.QUARTERLY,
        r'\bfel(ev|eve)nte\b': Frequency.EVERY_HALF_YEAR,
        r'\bminden fel(ev|eve)ben\b': Frequency.EVERY_HALF_YEAR,
        r'\b(ev|eve)nte\b': Frequency.YEARLY,
        r'\bminden (ev|eve)ben\b': Frequency.YEARLY,
        r'\b(ev|eve)(i|it|s)\b': Frequency.YEARLY,
    }

    for pattern, freq_value in frequency_map.items():
        match = re.search(pattern, s_no_accent)
        if match:
            return {
                "frequency": freq_value,
                "start": match.start(),
                "end": match.end()
            }

    return None
