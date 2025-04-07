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


def parse_frequency(s: str) -> Optional[str]:
    """
    Returns the frequency value found in the input string.

    :param s: Input string containing the frequency information in Hungarian.
    :return: The standardized frequency value as a string, or None if no valid frequency is found.
    """
    s = s.lower().strip()
    s_no_accent = remove_accent(s)

    frequency_map = {
        r'\bnap(onta|i|onkent)\b': Frequency.DAILY,
        r'\bminden nap\b': Frequency.DAILY,
        r'\bhet(ente|i|enkent)\b': Frequency.WEEKLY,
        r'\bminden het(en|eben)\b': Frequency.WEEKLY,
        r'\bheti rendszeresseg(gel)?\b': Frequency.WEEKLY,
        r'\bkethet(ente|i|enkent)\b': Frequency.FORTNIGHTLY,
        r'\bhav(onta|i|onkent)\b': Frequency.MONTHLY,
        r'\bhavi rendszeresseg(gel)?\b': Frequency.MONTHLY,
        r'\bnegyed(ev|eve)nte\b': Frequency.QUARTERLY,
        r'\bharomhav(onta|i)\b': Frequency.QUARTERLY,
        r'\bminden negyed(ev|eve)ben\b': Frequency.QUARTERLY,
        r'\bfel(ev|eve)nte\b': Frequency.EVERY_HALF_YEAR,
        r'\bminden fel(ev|eve)ben\b': Frequency.EVERY_HALF_YEAR,
        r'\b(ev|eve)nte\b': Frequency.YEARLY,
        r'\bminden (ev|eve)ben\b': Frequency.YEARLY,
    }

    for pattern, freq_value in frequency_map.items():
        if re.search(pattern, s_no_accent):
            return freq_value

    return None
