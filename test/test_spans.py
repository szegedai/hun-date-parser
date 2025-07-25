import pytest
from datetime import datetime

from hun_date_parser.date_parser.date_parsers import (
    match_iso_date, match_named_month, match_relative_day,
    match_weekday, match_week, match_named_year, match_relative_month,
    match_n_periods_compared_to_now, match_in_past_n_periods,
    match_date_offset, match_day_of_month, match_named_month_interval,
    match_named_month_start_mid_end
)
from hun_date_parser.utils import SearchScopes


# Test cases: (input_string, [(expected_match_text, expected_start, expected_end), ...])
# These are simplified test cases with known working patterns
tf_iso_date_spans = [
    ('2020-01-15', [('2020-01-15', 0, 10)]),
    ('legyen 2020-01 elején', [('2020-01', 7, 14)]),
    ('2020-12-30-án', [('2020-12-30', 0, 10)]),
    ('abcd 2020 1 15 abd', [('2020 1 15', 5, 14)]),
    ('2020 01 15', [('2020 01 15', 0, 10)]),
]

tf_named_month_spans = [
    ('január', [('január', 0, 6)]),
    ('februar', [('februar', 0, 7)]),
    ('februárban', [('február', 0, 7)]),
    ('márciustól', [('március', 0, 7)]),
    ('jan', [('jan', 0, 3)]),
    ('febr.', [('febr.', 0, 5)]),
    ('ápr 15', [('ápr 15', 0, 6)]),
    ('május 15', [('május 15', 0, 8)]),
    ('jan 20-án', [('jan 20', 0, 6)]),
    ('találkozunk májusban', [('május', 12, 17)]),
    ('2020 febr. 4-én volt', [('febr. 4', 5, 12)]),
]

tf_relative_day_spans = [
    ('ma', [('ma', 0, 2)]),
    ('holnap', [('holnap', 0, 6)]),
    ('tegnap', [('tegnap', 0, 6)]),
    ('holnapután', [('holnapután', 0, 10)]),
    ('ma-holnap', [('ma', 0, 2), ('holnap', 3, 9)]),
    ('legyen ma reggel', [('ma', 7, 9)]),
    ('miért nem jöttél tegnap', [('tegnap', 17, 23)]),
]

tf_weekday_spans = [
    ('hétfőn', [('hétfő', 0, 5)]),
    ('kedden', [('kedd', 0, 4)]),
    ('szombaton', [('szombat', 0, 7)]),
    ('múlt vasárnap', [('múlt vasárnap', 0, 13)]),
    ('jövő kedden', [('jövő kedd', 0, 9)]),
    ('szombaton ráérek', [('szombat', 0, 7)]),
    ('mit szólnál hétfőhöz', [('hétfő', 12, 17)]),
    ('jövő héten szerdán', [('jövő héten szerdá', 0, 17)]),
]

tf_week_spans = [
    ('ezen a héten', [('ezen a hét', 0, 10)]),
    ('múlt héten', [('múlt hét', 0, 8)]),
    ('jövő héten', [('jövő hét', 0, 8)]),
    ('múlthéten volt', [('múlthét', 0, 7)]),
]

tf_named_year_spans = [
    ('idén', [('idén', 0, 4)]),
    ('tavaly', [('tavaly', 0, 6)]),
    ('jövőre', [('jövőre', 0, 6)]),
    ('tavalyelőtt', [('tavalyelőtt', 0, 11)]),
    ('találkozunk jövőre', [('jövőre', 12, 18)]),
]

tf_relative_month_spans = [
    ('ebben a hónapban', [('ebben a hónap', 0, 13)]),
    ('múlt hónapban', [('múlt hónap', 0, 10)]),
    ('jövő hónapban', [('jövő hónap', 0, 10)]),
    ('az aktuális hónap', [('aktuális hónap', 3, 17)]),
    ('következő hónap', [('következő hónap', 0, 15)]),
]

tf_day_of_month_spans = [
    ('5-én', [('5-én', 0, 4)]),
    ('15-én', [('15-én', 0, 5)]),
    ('elsején', [('elsején', 0, 7)]),
    ('másodikán', [('másodikán', 0, 9)]),
    ('harmadikán', [('harmadikán', 0, 10)]),
    ('találkozunk 15-én', [('15-én', 12, 17)]),
    ('találkozunk elsején', [('elsején', 12, 19)]),
]

tf_n_periods_spans = [
    ('3 nap múlva', [('3 nap múlva', 0, 11)]),
    ('5 nappal ezelőtt', [('5 nappal ezelőtt', 0, 16)]),
    ('egy hét múlva', [('egy hét múlva', 0, 13)]),
    ('két héttel korábban', [('két héttel korábban', 0, 19)]),
    ('6 nappal ezelőtt', [('6 nappal ezelőtt', 0, 16)]),
]

# Additional test categories
tf_date_offset_spans = [
    ('5 napig', [('5', 0, 1)]),
    ('öt napig', [('öt', 0, 2)]),
    ('egy hétig', [('egy hét', 0, 7)]),
    ('3 hét', [('3 hét', 0, 5)]),
]

tf_past_periods_spans = [
    ('elmúlt egy hét', [('elmúlt egy hét', 0, 14)]),
    ('az előző két hét', [('előző két hét', 3, 16)]),
    ('az előző 10 nap', [('előző 10 nap', 3, 15)]),
]

tf_month_sme_spans = [
    ('jan eleje', [('jan elej', 0, 8)]),
    ('február közepe', [('február közep', 0, 13)]),
    ('március vége', [('március vég', 0, 11)]),
    ('január közepén', [('január közep', 0, 12)]),
]


@pytest.mark.parametrize("inp,expected_spans", tf_iso_date_spans)
def test_iso_date_spans(inp, expected_spans):
    """Test that ISO date matching returns correct span information."""
    out = match_iso_date(inp)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_named_month_spans)
def test_named_month_spans(inp, expected_spans):
    """Test that named month matching returns correct span information."""
    now = datetime(2020, 10, 1)
    out = match_named_month(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_relative_day_spans)
def test_relative_day_spans(inp, expected_spans):
    """Test that relative day matching returns correct span information."""
    now = datetime(2020, 10, 1)
    out = match_relative_day(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_weekday_spans)
def test_weekday_spans(inp, expected_spans):
    """Test that weekday matching returns correct span information."""
    now = datetime(2020, 12, 11)  # friday
    out = match_weekday(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_week_spans)
def test_week_spans(inp, expected_spans):
    """Test that week matching returns correct span information."""
    now = datetime(2020, 12, 7)
    out = match_week(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_named_year_spans)
def test_named_year_spans(inp, expected_spans):
    """Test that named year matching returns correct span information."""
    now = datetime(2020, 12, 7)
    out = match_named_year(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_relative_month_spans)
def test_relative_month_spans(inp, expected_spans):
    """Test that relative month matching returns correct span information."""
    now = datetime(2020, 12, 7)
    out = match_relative_month(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_day_of_month_spans)
def test_day_of_month_spans(inp, expected_spans):
    """Test that day of month matching returns correct span information."""
    now = datetime(2020, 12, 7)
    out = match_day_of_month(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_n_periods_spans)
def test_n_periods_compared_to_now_spans(inp, expected_spans):
    """Test that n periods matching returns correct span information."""
    now = datetime(2020, 12, 7)
    out = match_n_periods_compared_to_now(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_date_offset_spans)
def test_date_offset_spans(inp, expected_spans):
    """Test that date offset matching returns correct span information."""
    out = match_date_offset(inp)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_past_periods_spans)
def test_past_periods_spans(inp, expected_spans):
    """Test that past periods matching returns correct span information."""
    now = datetime(2023, 5, 20)
    out = match_in_past_n_periods(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


@pytest.mark.parametrize("inp,expected_spans", tf_month_sme_spans)
def test_month_start_mid_end_spans(inp, expected_spans):
    """Test that month start/mid/end matching returns correct span information."""
    now = datetime(2020, 10, 1)
    out = match_named_month_start_mid_end(inp, now)
    actual_spans = [(result['match_text'], result['match_start'], result['match_end']) for result in out]
    assert actual_spans == expected_spans


def test_span_fields_exist():
    """Test that all span-related fields exist in the output."""
    now = datetime(2020, 10, 1)
    test_input = 'találkozunk májusban'
    
    result = match_named_month(test_input, now)
    assert len(result) == 1
    
    match_result = result[0]
    
    # Check that all expected span fields exist
    assert 'match_text' in match_result
    assert 'match_start' in match_result
    assert 'match_end' in match_result
    
    # Check that values are correct types
    assert isinstance(match_result['match_text'], str)
    assert isinstance(match_result['match_start'], int)
    assert isinstance(match_result['match_end'], int)
    
    # Check that indices make sense
    assert match_result['match_start'] >= 0
    assert match_result['match_end'] > match_result['match_start']
    assert match_result['match_text'] == test_input[match_result['match_start']:match_result['match_end']]


def test_multiple_matches_spans():
    """Test that multiple matches in the same string have correct spans."""
    test_input = 'ma és holnap'
    now = datetime(2020, 10, 1)
    
    result = match_relative_day(test_input, now)
    assert len(result) == 2
    
    # First match: 'ma'
    assert result[0]['match_text'] == 'ma'
    assert result[0]['match_start'] == 0
    assert result[0]['match_end'] == 2
    
    # Second match: 'holnap'
    assert result[1]['match_text'] == 'holnap'
    assert result[1]['match_start'] == 6
    assert result[1]['match_end'] == 12


def test_overlapping_context_spans():
    """Test spans in longer context with surrounding text."""
    test_input = 'találkozunk holnap délután'
    now = datetime(2020, 10, 1)
    
    result = match_relative_day(test_input, now)
    assert len(result) == 1
    
    # Should match 'holnap' at the correct position
    assert result[0]['match_text'] == 'holnap'
    assert result[0]['match_start'] == 12
    assert result[0]['match_end'] == 18
    
    # Verify the substring matches
    extracted = test_input[result[0]['match_start']:result[0]['match_end']]
    assert extracted == 'holnap'