from datetime import datetime

from src.date_parser.structure_parsers import match_multi_match, match_interval
from src.date_parser.date_parsers import match_named_month, match_iso_date


def match_rules(sentence: str):
    return match_named_month(sentence) + match_iso_date(sentence)


class DateExtractor:

    def __init__(self):
        self.now = datetime.now()

    def _get_implicit_intervall(self, sentence_part: str):
        matches = match_rules(sentence_part)

        intervals = []
        for match in matches:
            intervals.append({'start_date': match['date_parts'], 'end_date': match['date_parts']})

        return intervals

    def parse_date(self, sentence: str):
        sentence_parts = match_multi_match(sentence)
        parsed_dates = []

        for sentence_part in sentence_parts:
            interval = match_interval(sentence_part)

            if interval:
                interval['start_date'] = match_rules(interval['start_date'])[0]['date_parts']
                interval['end_date'] = match_rules(interval['end_date'])[0]['date_parts']
                parsed_dates.append(interval)
            else:
                parsed_dates += self._get_implicit_intervall(sentence_part)

        return parsed_dates


if __name__ == '__main__':
    de = DateExtractor()
    print(de.parse_date('most januárban, februárban vagy 2020-10-12-tol 2020-11-01-ig'))
