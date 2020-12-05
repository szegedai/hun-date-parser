import re

from typing import Dict, List

from .patterns import R_MULTI, R_TOLIG, R_TOL, R_IG


def match_multi_match(s: str) -> List[str]:
    match = re.match(R_MULTI, s)

    if match:
        groups = match.groups()
        groups = [m.rstrip().lstrip() for m in groups if m]

        return groups

    return [s]


def match_interval(s: str) -> Dict:
    match = re.match(R_TOLIG, s)
    if match:
        groups = match.groups()
        groups = [m.lstrip().rstrip() for m in groups if m]

        if len(groups) == 2:
            return {
                'start_date': groups[0],
                'end_date': groups[1]
            }

    match = re.match(R_TOL, s)
    if match:
        groups = match.groups()
        groups = [m.lstrip().rstrip() for m in groups if m]

        if len(groups) == 1:
            return {
                'start_date': groups[0],
                'end_date': 'OPEN'
            }

    match = re.match(R_IG, s)
    if match:
        groups = match.groups()
        groups = [m.lstrip().rstrip() for m in groups if m]

        if len(groups) == 1:
            return {
                'start_date': 'OPEN',
                'end_date': groups[0]
            }

    return {}
