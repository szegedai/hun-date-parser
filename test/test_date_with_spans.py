import pytest
from datetime import datetime, date

from hun_date_parser.date_parser.datetime_extractor import text2date_with_spans


test_cases_with_spans = [
    ('találkozzunk szombaton', [
        {'match_text': 'szombat', 'match_start': 13, 'match_end': 20, 'date_range': [date(2020, 12, 19), date(2020, 12, 19)]}
    ]),
    ('január 5-én', [
        {'match_text': 'január 5-én', 'match_start': 0, 'match_end': 11, 'date_range': [date(2020, 1, 5), date(2020, 1, 5)]}
    ]),
    ('majd január 5-én', [
        {'match_text': 'január 5-én', 'match_start': 5, 'match_end': 16, 'date_range': [date(2020, 1, 5), date(2020, 1, 5)]}
    ]),
    ('majd 2025-05-05-én', [
        {'match_text': '2025-05-05', 'match_start': 5, 'match_end': 15, 'date_range': [date(2025, 5, 5), date(2025, 5, 5)]}
    ]),
    ('majd májusban', [
        {'match_text': 'május', 'match_start': 5, 'match_end': 10, 'date_range': [date(2020, 5, 1), date(2020, 5, 31)]}
    ]),
    ('holnap', [
        {'match_text': 'holnap', 'match_start': 0, 'match_end': 6, 'date_range': [date(2020, 12, 19), date(2020, 12, 19)]}
    ]),
    ('találkozunk ma és holnap', [
        {'match_text': 'ma', 'match_start': 12, 'match_end': 14, 'date_range': [date(2020, 12, 18), date(2020, 12, 18)]},
        {'match_text': 'holnap', 'match_start': 18, 'match_end': 24, 'date_range': [date(2020, 12, 19), date(2020, 12, 19)]}
    ]),
    ('februárban', [
        {'match_text': 'február', 'match_start': 0, 'match_end': 7, 'date_range': [date(2020, 2, 1), date(2020, 2, 29)]}
    ]),
    ('X februárban Y ', [
        {'match_text': 'február', 'match_start': 2, 'match_end': 9, 'date_range': [date(2020, 2, 1), date(2020, 2, 29)]}
    ]),
    ('múlt héten', [
        {'match_text': 'múlt hét', 'match_start': 0, 'match_end': 8, 'date_range': [date(2020, 12, 7), date(2020, 12, 13)]}
    ]),
    ('a múlt héten', [
        {'match_text': 'múlt hét', 'match_start': 2, 'match_end': 10, 'date_range': [date(2020, 12, 7), date(2020, 12, 13)]}
    ]),
    ('5-én', [
        {'match_text': '5-én', 'match_start': 0, 'match_end': 4, 'date_range': [date(2020, 12, 5), date(2020, 12, 5)]}
    ]),
    ('2021 január 5', [
        {'match_text': '2021 január 5', 'match_start': 0, 'match_end': 13, 'date_range': [date(2021, 1, 5), date(2021, 1, 5)]}
    ]),
    ('ekkor: 2021-01-05', [
        {'match_text': '2021-01-05', 'match_start': 7, 'match_end': 17, 'date_range': [date(2021, 1, 5), date(2021, 1, 5)]}
    ]),
    ('idén márciusban', [
        {'match_text': 'idén március', 'match_start': 0, 'match_end': 12, 'date_range': [date(2020, 3, 1), date(2020, 3, 31)]}
    ]),
    ('ekkor: 2020 márciusban', [
        {'match_text': '2020 március', 'match_start': 7, 'match_end': 19, 'date_range': [date(2020, 3, 1), date(2020, 3, 31)]}
    ]),
    ('xy tegnap vagy holnap', [
        {'match_text': 'tegnap', 'match_start': 3, 'match_end': 9, 'date_range': [date(2020, 12, 17), date(2020, 12, 17)]},
        {'match_text': 'holnap', 'match_start': 15, 'match_end': 21, 'date_range': [date(2020, 12, 19), date(2020, 12, 19)]}
    ]),
    ('múlt hét kedden', [
        {'match_text': 'múlt hét kedd', 'match_start': 0, 'match_end': 13, 'date_range': [date(2020, 12, 8), date(2020, 12, 8)]}
    ]),
    ('2020-ban találkozunk áprilisban', [
        {'match_text': '2020-ban találkozunk április', 'match_start': 0, 'match_end': 28, 'date_range': [date(2020, 4, 1), date(2020, 4, 30)]}
    ]),
    ('tavaly decemberben', [
        {'match_text': 'tavaly december', 'match_start': 0, 'match_end': 15, 'date_range': [date(2019, 12, 1), date(2019, 12, 31)]}
    ]),
    ('március 15-én vagy 16-án', [
        {'match_text': 'március 15-én', 'match_start': 0, 'match_end': 13, 'date_range': [date(2020, 3, 15), date(2020, 3, 15)]},
        {'match_text': '16-án', 'match_start': 19, 'match_end': 24, 'date_range': [date(2020, 12, 16), date(2020, 12, 16)]}
    ]),
    ('elsején', [
        {'match_text': 'elsején', 'match_start': 0, 'match_end': 7, 'date_range': [date(2020, 12, 1), date(2020, 12, 1)]}
    ]),
    ('B elsején', [
        {'match_text': 'elsején', 'match_start': 2, 'match_end': 9, 'date_range': [date(2020, 12, 1), date(2020, 12, 1)]}
    ]),
    ('jövő héten szerdán', [
        {'match_text': 'jövő héten szerdá', 'match_start': 0, 'match_end': 17, 'date_range': [date(2020, 12, 23), date(2020, 12, 23)]}
    ]),
    ('projekt befejezése 5 nap múlva lesz', [
        {'match_text': '5 nap múlva', 'match_start': 19, 'match_end': 30, 'date_range': [date(2020, 12, 23), date(2020, 12, 23)]}
    ]),
    ('ünnepség március elején tartjuk', [
        {'match_text': 'március elej', 'match_start': 9, 'match_end': 21, 'date_range': [date(2020, 3, 1), date(2020, 3, 10)]}
    ]),
    ('karácsonyi vásár december végén nyílik', [
        {'match_text': 'december vég', 'match_start': 17, 'match_end': 29, 'date_range': [date(2020, 12, 20), date(2020, 12, 31)]}
    ]),
    ('programunk 2 hét múlva indul el', [
        {'match_text': '2 hét múlva', 'match_start': 11, 'match_end': 22, 'date_range': [date(2021, 1, 1), date(2021, 1, 1)]}
    ]),
]


@pytest.mark.parametrize("inp_txt, expected", test_cases_with_spans)
def test_text2date_with_spans(inp_txt, expected):
    now = datetime(2020, 12, 18)
    result = text2date_with_spans(inp_txt, now)
    
    assert len(result) == len(expected)
    
    for i, (actual, exp) in enumerate(zip(result, expected)):
        assert actual['match_text'] == exp['match_text']
        assert actual['match_start'] == exp['match_start']
        assert actual['match_end'] == exp['match_end']
        assert actual['start_date'] == exp['date_range'][0]
        assert actual['end_date'] == exp['date_range'][1]