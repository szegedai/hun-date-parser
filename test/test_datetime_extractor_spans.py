import pytest
from datetime import datetime

from hun_date_parser.date_parser.datetime_extractor import text2datetime_with_spans, text2datetime


test_cases_with_spans = [
    ('találkozzunk szombaton', [
        {'match_text': 'szombat', 'match_start': 13, 'match_end': 20, 'datetime_range': [datetime(2020, 12, 19, 0, 0, 0), datetime(2020, 12, 19, 23, 59, 59)]}
    ]),
    ('január 5-én', [
        {'match_text': 'január 5-én', 'match_start': 0, 'match_end': 11, 'datetime_range': [datetime(2020, 1, 5, 0, 0, 0), datetime(2020, 1, 5, 23, 59, 59)]}
    ]),
    ('majd január 5-én', [
        {'match_text': 'január 5-én', 'match_start': 5, 'match_end': 16, 'datetime_range': [datetime(2020, 1, 5, 0, 0, 0), datetime(2020, 1, 5, 23, 59, 59)]}
    ]),
    ('majd 2025-05-05-én', [
        {'match_text': '2025-05-05', 'match_start': 5, 'match_end': 15, 'datetime_range': [datetime(2025, 5, 5, 0, 0, 0), datetime(2025, 5, 5, 23, 59, 59)]}
    ]),
    ('majd májusban', [
        {'match_text': 'május', 'match_start': 5, 'match_end': 10, 'datetime_range': [datetime(2020, 5, 1, 0, 0, 0), datetime(2020, 5, 31, 23, 59, 59)]}
    ]),
    ('holnap', [
        {'match_text': 'holnap', 'match_start': 0, 'match_end': 6, 'datetime_range': [datetime(2020, 12, 19, 0, 0, 0), datetime(2020, 12, 19, 23, 59, 59)]}
    ]),
    ('találkozunk ma és holnap', [
        {'match_text': 'ma', 'match_start': 12, 'match_end': 14, 'datetime_range': [datetime(2020, 12, 18, 0, 0, 0), datetime(2020, 12, 18, 23, 59, 59)]},
        {'match_text': 'holnap', 'match_start': 18, 'match_end': 24, 'datetime_range': [datetime(2020, 12, 19, 0, 0, 0), datetime(2020, 12, 19, 23, 59, 59)]}
    ]),
    ('februárban', [
        {'match_text': 'február', 'match_start': 0, 'match_end': 7, 'datetime_range': [datetime(2020, 2, 1, 0, 0, 0), datetime(2020, 2, 29, 23, 59, 59)]}
    ]),
    ('X februárban Y ', [
        {'match_text': 'február', 'match_start': 2, 'match_end': 9, 'datetime_range': [datetime(2020, 2, 1, 0, 0, 0), datetime(2020, 2, 29, 23, 59, 59)]}
    ]),
    ('múlt héten', [
        {'match_text': 'múlt hét', 'match_start': 0, 'match_end': 8, 'datetime_range': [datetime(2020, 12, 7, 0, 0, 0), datetime(2020, 12, 13, 23, 59, 59)]}
    ]),
    ('a múlt héten', [
        {'match_text': 'múlt hét', 'match_start': 2, 'match_end': 10, 'datetime_range': [datetime(2020, 12, 7, 0, 0, 0), datetime(2020, 12, 13, 23, 59, 59)]}
    ]),
    ('5-én', [
        {'match_text': '5-én', 'match_start': 0, 'match_end': 4, 'datetime_range': [datetime(2020, 12, 5, 0, 0, 0), datetime(2020, 12, 5, 23, 59, 59)]}
    ]),
    ('2021 január 5', [
        {'match_text': '2021 január 5', 'match_start': 0, 'match_end': 13, 'datetime_range': [datetime(2021, 1, 5, 0, 0, 0), datetime(2021, 1, 5, 23, 59, 59)]}
    ]),
    ('idén márciusban', [
        {'match_text': 'idén március', 'match_start': 0, 'match_end': 12, 'datetime_range': [datetime(2020, 3, 1, 0, 0, 0), datetime(2020, 3, 31, 23, 59, 59)]}
    ]),
    ('xy tegnap vagy holnap', [
        {'match_text': 'tegnap', 'match_start': 3, 'match_end': 9, 'datetime_range': [datetime(2020, 12, 17, 0, 0, 0), datetime(2020, 12, 17, 23, 59, 59)]},
        {'match_text': 'holnap', 'match_start': 15, 'match_end': 21, 'datetime_range': [datetime(2020, 12, 19, 0, 0, 0), datetime(2020, 12, 19, 23, 59, 59)]}
    ]),
    ('múlt hét kedden', [
        {'match_text': 'múlt hét kedd', 'match_start': 0, 'match_end': 13, 'datetime_range': [datetime(2020, 12, 8, 0, 0, 0), datetime(2020, 12, 8, 23, 59, 59)]}
    ]),
    ('2020-ban találkozunk áprilisban', [
        {'match_text': '2020-ban találkozunk április', 'match_start': 0, 'match_end': 28, 'datetime_range': [datetime(2020, 4, 1, 0, 0, 0), datetime(2020, 4, 30, 23, 59, 59)]}
    ]),
    ('tavaly decemberben', [
        {'match_text': 'tavaly december', 'match_start': 0, 'match_end': 15, 'datetime_range': [datetime(2019, 12, 1, 0, 0, 0), datetime(2019, 12, 31, 23, 59, 59)]}
    ]),
    ('március 15-én vagy 16-án', [
        {'match_text': 'március 15-én', 'match_start': 0, 'match_end': 13, 'datetime_range': [datetime(2020, 3, 15, 0, 0, 0), datetime(2020, 3, 15, 23, 59, 59)]},
        {'match_text': '16-án', 'match_start': 19, 'match_end': 24, 'datetime_range': [datetime(2020, 12, 16, 0, 0, 0), datetime(2020, 12, 16, 23, 59, 59)]}
    ]),
    ('elsején', [
        {'match_text': 'elsején', 'match_start': 0, 'match_end': 7, 'datetime_range': [datetime(2020, 12, 1, 0, 0, 0), datetime(2020, 12, 1, 23, 59, 59)]}
    ]),
    ('B elsején', [
        {'match_text': 'elsején', 'match_start': 2, 'match_end': 9, 'datetime_range': [datetime(2020, 12, 1, 0, 0, 0), datetime(2020, 12, 1, 23, 59, 59)]}
    ]),
    ('jövő héten szerdán', [
        {'match_text': 'jövő héten szerdá', 'match_start': 0, 'match_end': 17, 'datetime_range': [datetime(2020, 12, 23, 0, 0, 0), datetime(2020, 12, 23, 23, 59, 59)]}
    ]),
    ('január 5-én reggel', [
        {'match_text': 'január 5-én reggel', 'match_start': 0, 'match_end': 18, 'datetime_range': [datetime(2020, 1, 5, 6, 0, 0), datetime(2020, 1, 5, 10, 59, 59)]}
    ]),
    ('X január 5-én reggel', [
        {'match_text': 'január 5-én reggel', 'match_start': 2, 'match_end': 20, 'datetime_range': [datetime(2020, 1, 5, 6, 0, 0), datetime(2020, 1, 5, 10, 59, 59)]}
    ]),
    ('péntek este 8 óra', [
        {'match_text': 'péntek este 8 óra', 'match_start': 0, 'match_end': 17, 'datetime_range': [datetime(2020, 12, 18, 20, 0, 0), datetime(2020, 12, 18, 20, 59, 59)]}
    ]),
    ('Y péntek este 8 óra', [
        {'match_text': 'péntek este 8 óra', 'match_start': 2, 'match_end': 19, 'datetime_range': [datetime(2020, 12, 18, 20, 0, 0), datetime(2020, 12, 18, 20, 59, 59)]}
    ]),
    ('Y péntek este 8 óra X', [
        {'match_text': 'péntek este 8 óra', 'match_start': 2, 'match_end': 19, 'datetime_range': [datetime(2020, 12, 18, 20, 0, 0), datetime(2020, 12, 18, 20, 59, 59)]}
    ]),
    ('holnap délután 3-kor', [
        {'match_text': 'holnap délután 3-kor', 'match_start': 0, 'match_end': 20, 'datetime_range': [datetime(2020, 12, 19, 15, 0, 0), datetime(2020, 12, 19, 15, 59, 59)]}
    ]),
    ('x ma este 7-kor', [
        {'match_text': 'ma este 7-kor', 'match_start': 2, 'match_end': 15, 'datetime_range': [datetime(2020, 12, 18, 19, 0, 0), datetime(2020, 12, 18, 19, 59, 59)]}
    ]),
]


@pytest.mark.parametrize("inp_txt, expected", test_cases_with_spans)
def test_text2datetime_with_spans(inp_txt, expected):
    """Test that text2datetime_with_spans returns correct span information and datetime extraction."""
    now = datetime(2020, 12, 18)
    result = text2datetime_with_spans(inp_txt, now)

    print(result)
    
    assert len(result) == len(expected), f"Expected {len(expected)} matches, got {len(result)}"
    
    for i, (actual, exp) in enumerate(zip(result, expected)):
        assert actual['match_text'] == exp['match_text'], f"Match {i}: expected text '{exp['match_text']}', got '{actual['match_text']}'"
        assert actual['match_start'] == exp['match_start'], f"Match {i}: expected start {exp['match_start']}, got {actual['match_start']}"
        assert actual['match_end'] == exp['match_end'], f"Match {i}: expected end {exp['match_end']}, got {actual['match_end']}"
        
        # Verify span extraction matches actual text
        extracted_text = inp_txt[actual['match_start']:actual['match_end']]
        assert extracted_text == actual['match_text'], f"Match {i}: extracted text '{extracted_text}' doesn't match match_text '{actual['match_text']}'"
        
        # Check datetime objects if provided in expected
        if 'datetime_range' in exp:
            assert 'start_date' in actual, f"Match {i}: missing start_date"
            assert 'end_date' in actual, f"Match {i}: missing end_date"
            expected_start, expected_end = exp['datetime_range']
            assert actual['start_date'] == expected_start, f"Match {i}: expected start_date {expected_start}, got {actual['start_date']}"
            assert actual['end_date'] == expected_end, f"Match {i}: expected end_date {expected_end}, got {actual['end_date']}"


def test_text2datetime_with_spans_consistency():
    """Test that text2datetime_with_spans returns consistent results with text2datetime."""
    now = datetime(2020, 12, 18)
    test_sentences = [
        'találkozzunk holnap',
        'január 5-én',
        'múlt héten',
        'ma reggel',
        '2021 január 5',
    ]
    
    for sentence in test_sentences:
        spans_result = text2datetime_with_spans(sentence, now)
        regular_result = text2datetime(sentence, now)
        
        # Both should find the same number of matches
        assert len(spans_result) >= len(regular_result), f"Spans result should have at least as many matches as regular result for '{sentence}'"


def test_text2datetime_with_spans_empty_input():
    """Test that text2datetime_with_spans handles empty input correctly."""
    now = datetime(2020, 12, 18)
    result = text2datetime_with_spans('', now)
    assert result == []


def test_text2datetime_with_spans_no_matches():
    """Test that text2datetime_with_spans handles input with no date matches."""
    now = datetime(2020, 12, 18)
    result = text2datetime_with_spans('nincs itt semmi dátum', now)
    assert result == []


def test_text2datetime_with_spans_overlapping_matches():
    """Test that text2datetime_with_spans handles overlapping date expressions."""
    now = datetime(2020, 12, 18)
    result = text2datetime_with_spans('jövő hét hétfőn', now)
    
    # Should find at least one match
    assert len(result) >= 1
    
    # Verify all matches have valid span information
    for match in result:
        assert 'match_text' in match
        assert 'match_start' in match
        assert 'match_end' in match
        assert 'start_date' in match
        assert 'end_date' in match
        assert isinstance(match['match_start'], int)
        assert isinstance(match['match_end'], int)
        assert match['match_start'] >= 0
        assert match['match_end'] > match['match_start']


def test_text2datetime_with_spans_fields():
    """Test that text2datetime_with_spans returns all required fields."""
    now = datetime(2020, 12, 18)
    result = text2datetime_with_spans('holnap', now)
    
    assert len(result) == 1
    match = result[0]
    
    # Check all required fields exist
    required_fields = ['match_text', 'match_start', 'match_end', 'start_date', 'end_date']
    for field in required_fields:
        assert field in match, f"Missing required field: {field}"
    
    # Check field types
    assert isinstance(match['match_text'], str)
    assert isinstance(match['match_start'], int)
    assert isinstance(match['match_end'], int)
    assert isinstance(match['start_date'], datetime)
    assert isinstance(match['end_date'], datetime)
    
    # Check datetime logic
    assert match['start_date'] <= match['end_date'], "start_date should be <= end_date"