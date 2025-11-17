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
    ('ekkor: 2021-01-05', [
        {'match_text': '2021-01-05', 'match_start': 7, 'match_end': 17, 'datetime_range': [datetime(2021, 1, 5, 0, 0, 0), datetime(2021, 1, 5, 23, 59, 59)]}
    ]),
    ('idén márciusban', [
        {'match_text': 'idén március', 'match_start': 0, 'match_end': 12, 'datetime_range': [datetime(2020, 3, 1, 0, 0, 0), datetime(2020, 3, 31, 23, 59, 59)]}
    ]),
    ('ekkor: 2020 márciusban', [
        {'match_text': '2020 március', 'match_start': 7, 'match_end': 19, 'datetime_range': [datetime(2020, 3, 1, 0, 0, 0), datetime(2020, 3, 31, 23, 59, 59)]}
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
    ('időpont foglalása holnapra vagy legyen inkább holnapután', [
        {'match_text': 'holnap', 'match_start': 18, 'match_end': 24, 'datetime_range': [datetime(2020, 12, 19, 0, 0, 0), datetime(2020, 12, 19, 23, 59, 59)]},
        {'match_text': 'holnapután', 'match_start': 46, 'match_end': 56, 'datetime_range': [datetime(2020, 12, 20, 0, 0, 0), datetime(2020, 12, 20, 23, 59, 59)]}
    ]),
    ('találkozunk kedden este 8-kor vagy szerdán délelőtt', [
        {'match_text': 'kedden este 8-kor', 'match_start': 12, 'match_end': 29, 'datetime_range': [datetime(2020, 12, 15, 20, 0, 0), datetime(2020, 12, 15, 20, 59, 59)]},
        {'match_text': 'szerdán délelőtt', 'match_start': 35, 'match_end': 51, 'datetime_range': [datetime(2020, 12, 16, 8, 0, 0), datetime(2020, 12, 16, 11, 59, 59)]}
    ]),
    ('BBB hétfőn reggel 9-kor kezdjük', [
        {'match_text': 'hétfőn reggel 9-kor', 'match_start': 4, 'match_end': 23, 'datetime_range': [datetime(2020, 12, 14, 9, 0, 0), datetime(2020, 12, 14, 9, 59, 59)]}
    ]),
    ('Z március 5-én Y', [
        {'match_text': 'március 5-én', 'match_start': 2, 'match_end': 14, 'datetime_range': [datetime(2020, 3, 5, 0, 0, 0), datetime(2020, 3, 5, 23, 59, 59)]}
    ]),
    ('X múlt csütörtökön délután 3-kor X', [
        {'match_text': 'múlt csütörtökön délután 3-kor', 'match_start': 2, 'match_end': 32, 'datetime_range': [datetime(2020, 12, 10, 15, 0, 0), datetime(2020, 12, 10, 15, 59, 59)]}
    ]),
    ('az értekezlet 14:30-kor kezdődik', [
        {'match_text': '14:30', 'match_start': 14, 'match_end': 19, 'datetime_range': [datetime(2020, 12, 18, 14, 30, 0), datetime(2020, 12, 18, 14, 30, 59)]}
    ]),
    ('beszélgetés most folyik', [
        {'match_text': 'most', 'match_start': 12, 'match_end': 16, 'datetime_range': [datetime(2020, 12, 18, 0, 0, 0), datetime(2020, 12, 18, 0, 0, 59)]}
    ]),
    ('projekt befejezése 5 nap múlva lesz', [
        {'match_text': '5 nap múlva', 'match_start': 19, 'match_end': 30, 'datetime_range': [datetime(2020, 12, 23, 0, 0, 0), datetime(2020, 12, 23, 23, 59, 59)]}
    ]),
    ('ünnepség március elején tartjuk', [
        {'match_text': 'március elej', 'match_start': 9, 'match_end': 21, 'datetime_range': [datetime(2020, 3, 1, 0, 0, 0), datetime(2020, 3, 10, 23, 59, 59)]}
    ]),
    ('karácsonyi vásár december végén nyílik', [
        {'match_text': 'december vég', 'match_start': 17, 'match_end': 29, 'datetime_range': [datetime(2020, 12, 20, 0, 0, 0), datetime(2020, 12, 31, 23, 59, 59)]}
    ]),
    ('programunk 2 hét múlva indul el', [
        {'match_text': '2 hét múlva', 'match_start': 11, 'match_end': 22, 'datetime_range': [datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 1, 1, 23, 59, 59)]}
    ]),
    ('konferencia rendezése 16h-kor zárul', [
        {'match_text': '16h', 'match_start': 22, 'match_end': 25, 'datetime_range': [datetime(2020, 12, 18, 16, 0, 0), datetime(2020, 12, 18, 16, 59, 59)]}
    ]),
    # Additional test cases with random characters before/after target spans
    ('xyz hétfőn találkozunk abc', [
        {'match_text': 'hétfő', 'match_start': 4, 'match_end': 9, 'datetime_range': [datetime(2020, 12, 14, 0, 0, 0), datetime(2020, 12, 14, 23, 59, 59)]}
    ]),
    ('qwe kedden dolgozom rty', [
        {'match_text': 'kedd', 'match_start': 4, 'match_end': 8, 'datetime_range': [datetime(2020, 12, 15, 0, 0, 0), datetime(2020, 12, 15, 23, 59, 59)]}
    ]),
    ('abc múlt vasárnap voltunk ott xyz', [
        {'match_text': 'múlt vasárnap', 'match_start': 4, 'match_end': 17, 'datetime_range': [datetime(2020, 12, 13, 0, 0, 0), datetime(2020, 12, 13, 23, 59, 59)]}
    ]),
    ('def jövő kedden indulunk ghi', [
        {'match_text': 'jövő kedd', 'match_start': 4, 'match_end': 13, 'datetime_range': [datetime(2020, 12, 22, 0, 0, 0), datetime(2020, 12, 22, 23, 59, 59)]}
    ]),
    ('pqr harmadikán megyünk uvw', [
        {'match_text': 'harmadikán', 'match_start': 4, 'match_end': 14, 'datetime_range': [datetime(2020, 12, 3, 0, 0, 0), datetime(2020, 12, 3, 23, 59, 59)]}
    ]),
    ('zyx 15-én van a meeting stu', [
        {'match_text': '15-én', 'match_start': 4, 'match_end': 9, 'datetime_range': [datetime(2020, 12, 15, 0, 0, 0), datetime(2020, 12, 15, 23, 59, 59)]}
    ]),
    ('mno 2021-ben történt vwx', [
        {'match_text': '2021', 'match_start': 4, 'match_end': 8, 'datetime_range': [datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 12, 31, 23, 59, 59)]}
    ]),
    ('abc tavaly decemberben def', [
        {'match_text': 'tavaly december', 'match_start': 4, 'match_end': 19, 'datetime_range': [datetime(2019, 12, 1, 0, 0, 0), datetime(2019, 12, 31, 23, 59, 59)]}
    ]),
    ('klm jövő évben találkozunk opq', [
        {'match_text': 'jövő évben', 'match_start': 4, 'match_end': 14, 'datetime_range': [datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 12, 31, 23, 59, 59)]}
    ]),
    ('rst 3 hét múlva utazunk xyz', [
        {'match_text': '3 hét múlva', 'match_start': 4, 'match_end': 15, 'datetime_range': [datetime(2021, 1, 8, 0, 0, 0), datetime(2021, 1, 8, 23, 59, 59)]}
    ]),
    ('vbn február közepén mnb', [
        {'match_text': 'február közep', 'match_start': 4, 'match_end': 17, 'datetime_range': [datetime(2020, 2, 10, 0, 0, 0), datetime(2020, 2, 20, 23, 59, 59)]}
    ]),
    # Test cases for -tól/től suffix fix (open intervals)
    ('ettől az évtől', [
        {'match_text': 'ettől az évtől', 'match_start': 0, 'match_end': 14, 'datetime_range': [datetime(2020, 1, 1, 0, 0, 0), None]}
    ]),
    ('idei évtől', [
        {'match_text': 'idei évtől', 'match_start': 0, 'match_end': 10, 'datetime_range': [datetime(2020, 1, 1, 0, 0, 0), None]}
    ]),
    ('ebben az évben találkozunk', [
        {'match_text': 'ebben az évben', 'match_start': 0, 'match_end': 14, 'datetime_range': [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 12, 31, 23, 59, 59)]}
    ]),
    ('xyz ettől az évtől abc', [
        {'match_text': 'ettől az évtől', 'match_start': 4, 'match_end': 18, 'datetime_range': [datetime(2020, 1, 1, 0, 0, 0), None]}
    ]),
    ('múlt évtől kezdve', [
        {'match_text': 'múlt évtől', 'match_start': 0, 'match_end': 10, 'datetime_range': [datetime(2019, 1, 1, 0, 0, 0), None]}
    ]),
    ('jövő évtől', [
        {'match_text': 'jövő évtől', 'match_start': 0, 'match_end': 10, 'datetime_range': [datetime(2021, 1, 1, 0, 0, 0), None]}
    ]),
    # Additional test cases for interval expressions
    ('januártól februárig', [
        {'match_text': 'januártól február', 'match_start': 0, 'match_end': 17, 'datetime_range': [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 2, 29, 23, 59, 59)]}
    ]),
    ('májusig', [
        {'match_text': 'májusig', 'match_start': 0, 'match_end': 7, 'datetime_range': [None, datetime(2020, 5, 31, 23, 59, 59)]}
    ]),
    # Test cases for duration expressions
    ('holnaptól 3 napig', [
        {'match_text': 'holnaptól 3 napig', 'match_start': 0, 'match_end': 17, 'datetime_range': [datetime(2020, 12, 19, 0, 0, 0), datetime(2020, 12, 22, 23, 59, 59)]}
    ]),
    ('ma 2 órára', [
        {'match_text': 'ma', 'match_start': 0, 'match_end': 2, 'datetime_range': [datetime(2020, 12, 18, 0, 0, 0), datetime(2020, 12, 18, 23, 59, 59)]}
    ]),
    # Test cases with unrealistic years for realistic_year_required testing
    ('találkozzunk 1850 január 5-én', [
        {'match_text': 'január 5-én', 'match_start': 18, 'match_end': 29, 'datetime_range': [datetime(2020, 1, 5, 0, 0, 0), datetime(2020, 1, 5, 23, 59, 59)]}
    ]),
    ('legyen 2150 december 31-én', [
        {'match_text': 'december 31-én', 'match_start': 12, 'match_end': 26, 'datetime_range': [datetime(2020, 12, 31, 0, 0, 0), datetime(2020, 12, 31, 23, 59, 59)]}
    ]),
    # Test cases for multiple expressions in one sentence
    ('ráérek kedden vagy szerdán', [
        {'match_text': 'kedd', 'match_start': 7, 'match_end': 11, 'datetime_range': [datetime(2020, 12, 15, 0, 0, 0), datetime(2020, 12, 15, 23, 59, 59)]},
        {'match_text': 'szerdá', 'match_start': 19, 'match_end': 25, 'datetime_range': [datetime(2020, 12, 16, 0, 0, 0), datetime(2020, 12, 16, 23, 59, 59)]}
    ]),
    ('találkozzunk februárban és augusztusban', [
        {'match_text': 'február', 'match_start': 13, 'match_end': 20, 'datetime_range': [datetime(2020, 2, 1, 0, 0, 0), datetime(2020, 2, 29, 23, 59, 59)]},
        {'match_text': 'augusztus', 'match_start': 27, 'match_end': 36, 'datetime_range': [datetime(2020, 8, 1, 0, 0, 0), datetime(2020, 8, 31, 23, 59, 59)]}
    ]),
    # Edge cases and boundary conditions
    ('december 31-én éjfélkor', [
        {'match_text': 'december 31-én', 'match_start': 0, 'match_end': 14, 'datetime_range': [datetime(2020, 12, 31, 0, 0, 0), datetime(2020, 12, 31, 23, 59, 59)]}
    ]),
    ('január 1-jén hajnalban', [
        {'match_text': 'január 1-jén hajnal', 'match_start': 0, 'match_end': 19, 'datetime_range': [datetime(2020, 1, 1, 3, 0, 0), datetime(2020, 1, 1, 5, 59, 59)]}
    ]),
    # Test cases from other test files
    ('ezen a héten', [
        {'match_text': 'ezen a hét', 'match_start': 0, 'match_end': 10, 'datetime_range': [datetime(2020, 12, 14, 0, 0, 0), datetime(2020, 12, 20, 23, 59, 59)]}
    ]),
    ('előző két napban dolgozom', [
        {'match_text': 'előző két napban', 'match_start': 0, 'match_end': 16, 'datetime_range': [datetime(2020, 12, 16, 0, 0, 0), datetime(2020, 12, 18, 0, 0, 0)]}
    ]),
    ('megelőző két hónap', [
        {'match_text': 'megelőző két hónap', 'match_start': 0, 'match_end': 18, 'datetime_range': [datetime(2020, 10, 18, 0, 0, 0), datetime(2020, 12, 18, 0, 0, 0)]}
    ]),

]


@pytest.mark.parametrize("inp_txt, expected", test_cases_with_spans)
def test_text2datetime_with_spans(inp_txt, expected):
    """Test that text2datetime_with_spans returns correct span information and datetime extraction."""
    now = datetime(2020, 12, 18)
    result = text2datetime_with_spans(inp_txt, now)

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


# Test cases for different search scopes
search_scope_cases = [
    # (input_text, search_scope, expected_results)
    ('hétfőn', 'PAST_SEARCH', [
        {'match_text': 'hétfő', 'match_start': 0, 'match_end': 5, 'datetime_range': [datetime(2020, 12, 14, 0, 0, 0), datetime(2020, 12, 14, 23, 59, 59)]}
    ]),
    ('hétfőn', 'FUTURE_DAY', [
        {'match_text': 'hétfő', 'match_start': 0, 'match_end': 5, 'datetime_range': [datetime(2020, 12, 21, 0, 0, 0), datetime(2020, 12, 21, 23, 59, 59)]}
    ]),
    ('kedden dolgozom', 'PAST_SEARCH', [
        {'match_text': 'kedd', 'match_start': 0, 'match_end': 4, 'datetime_range': [datetime(2020, 12, 15, 0, 0, 0), datetime(2020, 12, 15, 23, 59, 59)]}
    ]),
    ('találkozzunk kedden', 'FUTURE_DAY', [
        {'match_text': 'kedd', 'match_start': 13, 'match_end': 17, 'datetime_range': [datetime(2020, 12, 22, 0, 0, 0), datetime(2020, 12, 22, 23, 59, 59)]}
    ]),
    ('ráérek csütörtökön', 'PAST_SEARCH', [
        {'match_text': 'csütörtök', 'match_start': 7, 'match_end': 16, 'datetime_range': [datetime(2020, 12, 17, 0, 0, 0), datetime(2020, 12, 17, 23, 59, 59)]}
    ]),
    ('legyen szerdán reggel', 'FUTURE_DAY', [
        {'match_text': 'szerdán reggel', 'match_start': 7, 'match_end': 21, 'datetime_range': [datetime(2020, 12, 23, 6, 0, 0), datetime(2020, 12, 23, 10, 59, 59)]}
    ]),
]

@pytest.mark.parametrize("inp_txt, scope_name, expected", search_scope_cases)
def test_text2datetime_with_spans_search_scopes(inp_txt, scope_name, expected):
    """Test that text2datetime_with_spans works with different search scopes."""
    from hun_date_parser.utils import SearchScopes
    now = datetime(2020, 12, 18)  # Friday
    
    scope = getattr(SearchScopes, scope_name)
    result = text2datetime_with_spans(inp_txt, now, search_scope=scope)
    
    assert len(result) == len(expected), f"Expected {len(expected)} matches, got {len(result)}"
    
    for i, (actual, exp) in enumerate(zip(result, expected)):
        assert actual['match_text'] == exp['match_text'], f"Match {i}: expected text '{exp['match_text']}', got '{actual['match_text']}'"
        assert actual['match_start'] == exp['match_start'], f"Match {i}: expected start {exp['match_start']}, got {actual['match_start']}"
        assert actual['match_end'] == exp['match_end'], f"Match {i}: expected end {exp['match_end']}, got {actual['match_end']}"
        
        expected_start, expected_end = exp['datetime_range']
        assert actual['start_date'] == expected_start, f"Match {i}: expected start_date {expected_start}, got {actual['start_date']}"
        assert actual['end_date'] == expected_end, f"Match {i}: expected end_date {expected_end}, got {actual['end_date']}"


# Test cases for realistic_year_required parameter
realistic_year_cases = [
    # (input_text, realistic_year_required, expected_results)
    ('találkozzunk 1850 január 5-én', False, [
        {'match_text': '1850 január 5-én', 'match_start': 13, 'match_end': 29, 'datetime_range': [datetime(1850, 1, 5, 0, 0, 0), datetime(1850, 1, 5, 23, 59, 59)]}
    ]),
    ('találkozzunk 1850 január 5-én', True, [
        {'match_text': 'január 5-én', 'match_start': 18, 'match_end': 29, 'datetime_range': [datetime(2020, 1, 5, 0, 0, 0), datetime(2020, 1, 5, 23, 59, 59)]}
    ]),  # Year rejected, but month-day accepted
    ('legyen 2150 december 31-én', False, [
        {'match_text': '2150 december 31-én', 'match_start': 7, 'match_end': 26, 'datetime_range': [datetime(2150, 12, 31, 0, 0, 0), datetime(2150, 12, 31, 23, 59, 59)]}
    ]),
    ('legyen 2150 december 31-én', True, [
        {'match_text': 'december 31-én', 'match_start': 12, 'match_end': 26, 'datetime_range': [datetime(2020, 12, 31, 0, 0, 0), datetime(2020, 12, 31, 23, 59, 59)]}
    ]),  # Year rejected, but month-day accepted
    ('ráérek 2021 március 15-én', False, [
        {'match_text': '2021 március 15-én', 'match_start': 7, 'match_end': 25, 'datetime_range': [datetime(2021, 3, 15, 0, 0, 0), datetime(2021, 3, 15, 23, 59, 59)]}
    ]),
    ('ráérek 2021 március 15-én', True, [
        {'match_text': '2021 március 15-én', 'match_start': 7, 'match_end': 25, 'datetime_range': [datetime(2021, 3, 15, 0, 0, 0), datetime(2021, 3, 15, 23, 59, 59)]}
    ]),  # Should be accepted (realistic year)
]

@pytest.mark.parametrize("inp_txt, realistic_required, expected", realistic_year_cases)
def test_text2datetime_with_spans_realistic_year_required(inp_txt, realistic_required, expected):
    """Test that text2datetime_with_spans respects realistic_year_required parameter."""
    now = datetime(2020, 12, 18)
    result = text2datetime_with_spans(inp_txt, now, realistic_year_required=realistic_required)
    
    assert len(result) == len(expected), f"Expected {len(expected)} matches, got {len(result)}"
    
    for i, (actual, exp) in enumerate(zip(result, expected)):
        assert actual['match_text'] == exp['match_text'], f"Match {i}: expected text '{exp['match_text']}', got '{actual['match_text']}'"
        assert actual['match_start'] == exp['match_start'], f"Match {i}: expected start {exp['match_start']}, got {actual['match_start']}"
        assert actual['match_end'] == exp['match_end'], f"Match {i}: expected end {exp['match_end']}, got {actual['match_end']}"
        
        expected_start, expected_end = exp['datetime_range']
        assert actual['start_date'] == expected_start, f"Match {i}: expected start_date {expected_start}, got {actual['start_date']}"
        assert actual['end_date'] == expected_end, f"Match {i}: expected end_date {expected_end}, got {actual['end_date']}"