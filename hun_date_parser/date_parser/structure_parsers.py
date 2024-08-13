import re

from typing import Dict, List

from .patterns import (R_MULTI, R_TOLIG, R_TOL, R_IG, R_NAPRA_TOL, R_TOL_NAPRA, R_TOLIG_IMPLIED_END,
                       R_START_STATED_END_IMPLIED, R_TOLIG_Y, R_TOLIG_YMD, R_TOLIG_MD, R_TOLIG_YM, R_TOLIG_M)


def match_multi_match(s: str):
    match = re.match(R_MULTI, s)

    # If any of these are matched,
    # shouldn't count the input as having multiple matches which need to be parsed separately
    excluding_matches = [
        re.findall(R_TOL_NAPRA, s),
        re.findall(R_NAPRA_TOL, s),
    ]

    if match and not any(excluding_matches):
        groups = match.groups()
        groups = [m.rstrip().lstrip() for m in groups if m]

        return groups

    return [s]


def match_interval(s: str) -> Dict:
    # If any of these are matched,
    # shouldn't count the input as having multiple matches which need to be parsed separately
    excluding_matches = [
        re.findall(R_TOLIG_IMPLIED_END, s)
    ]

    if any(excluding_matches):
        return {}

    match = re.match(R_START_STATED_END_IMPLIED, s)
    if match:
        groups = match.groups()
        groups = [m.lstrip().rstrip() for m in groups if m]

        if len(groups) == 2:
            return {
                'start_date': groups[0],
                'end_date': groups[1]
            }

    for regex in [R_TOLIG,
                  R_TOLIG_YMD,
                  R_TOLIG_YM,
                  R_TOLIG_MD,
                  R_TOLIG_Y,
                  R_TOLIG_M]:
        match = re.match(regex, s)
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
    match = re.match(R_TOL_NAPRA, s)
    if match:
        groups = match.groups()
        groups = [m.rstrip().lstrip() for m in groups if m]
        from_part, duration_part = groups

        return [from_part, duration_part]

    match = re.match(R_NAPRA_TOL, s)
    if match:
        groups = match.groups()
        groups = [m.rstrip().lstrip() for m in groups if m]
        duration_part, from_part = groups

        return [from_part, duration_part]

    return []
