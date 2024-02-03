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


def match_duration_match(s: str) -> List[str]:
    R_TOL_NAPRA = r"(.*-?t[oóöő]l\b)(.*(napra|napig)\b)"
    R_NAPRA_TOL = r"(.*(napra|napig)\b)(.*-?t[oóöő]l\b)"

    match = re.match(R_TOL_NAPRA, s)
    if match:
        groups = match.groups()
        groups = [m.rstrip().lstrip() for m in groups if m]
        from_part, duration_part, _ = groups

        return [from_part, duration_part]

    match = re.match(R_NAPRA_TOL, s)
    if match:
        groups = match.groups()
        groups = [m.rstrip().lstrip() for m in groups if m]
        duration_part, _, from_part = groups

        return [from_part, duration_part]

    return []
