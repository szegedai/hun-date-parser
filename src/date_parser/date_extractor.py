from datetime import datetime
from itertools import chain

from typing import Dict
from copy import copy

from src.date_parser.structure_parsers import match_multi_match, match_interval
from src.date_parser.date_parsers import (match_named_month, match_iso_date, match_weekday, match_relative_day,
                                          match_week)
from src.date_parser.time_parsers import match_digi_clock


def match_rules(sentence: str):
    matches = [*match_named_month(sentence),
            *match_iso_date(sentence),
            *match_relative_day(sentence, datetime.now()),
            *match_weekday(sentence, datetime.now()),
            *match_week(sentence, datetime.now()),
            *match_digi_clock(sentence)]

    matches = list(chain(*[m['date_parts'] for m in matches]))

    return matches


def extend_start_end(interval: Dict):
    interval_ = copy(interval)
    for dp in interval['start_date']:
        if type(dp) not in [type(d) for d in interval['end_date']]:
            interval_['end_date'].append(dp)

    return interval_


class DateExtractor:

    def __init__(self):
        self.now = datetime.now()

    def _get_implicit_intervall(self, sentence_part: str):
        matches = match_rules(sentence_part)

        return [{'start_date': matches, 'end_date': matches}]

    def parse_date(self, sentence: str):
        sentence_parts = match_multi_match(sentence)
        parsed_dates = []

        for sentence_part in sentence_parts:
            interval = match_interval(sentence_part)

            if interval:
                interval['start_date'] = match_rules(interval['start_date'])
                interval['end_date'] = match_rules(interval['end_date'])
                parsed_dates.append(interval)
            else:
                parsed_dates += self._get_implicit_intervall(sentence_part)

        parsed_dates = [extend_start_end(intv) for intv in parsed_dates]

        return parsed_dates


if __name__ == '__main__':
    de = DateExtractor()
    print(de.parse_date('most januárban, februárban vagy 2020-10-12-tol 2020-11-01-ig'))
    print(de.parse_date('most kedden, múlthét vasárnap'))
    print(de.parse_date('ma reggel 7:30-tól holnap 8:20-ig'))
