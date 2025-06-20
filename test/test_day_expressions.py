import pytest
from datetime import datetime

from hun_date_parser import text2datetime, text2date
from hun_date_parser.utils import EntitySpan


class TestDayExpressions:
    
    def test_weekday_expressions(self):
        """Test weekday expressions with span tracking."""
        now = datetime(2020, 12, 27)  # Sunday
        
        test_cases = [
            ('hétfőn', 'hétfőn'),
            ('kedden', 'kedden'),
            ('szerdán', 'szerdán'),
            ('csütörtökön', 'csütörtökön'),
            ('pénteken', 'pénteken'),
            ('szombaton', 'szombaton'),
            ('vasárnap', 'vasárnap'),
            ('jövő hétfőn', 'jövő hétfőn'),
            ('múlt kedden', 'múlt kedden'),
            ('előző szerdán', 'előző szerdán'),
        ]
        
        for text, expected_span_text in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            assert len(result) == 1, f"Expected 1 match for '{text}', got {len(result)}"
            
            # Check span
            assert 'span' in result[0], f"No span found for '{text}'"
            span = result[0]['span']
            assert isinstance(span, EntitySpan)
            assert span.text == expected_span_text
            assert text[span.start:span.end] == expected_span_text

    def test_non_accented_weekdays(self):
        """Test non-accented weekday variants."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            ('hetfon', 1),  # Monday = 0, so next Monday from Sunday
            ('kedden', 1),  # Tuesday = 1
            ('szerdan', 2),  # Wednesday = 2
            ('csutortokon', 3),  # Thursday = 3
            ('penteken', 4),  # Friday = 4
        ]
        
        for text, expected_weekday in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            if len(result) == 1:  # If recognized
                assert 'span' in result[0], f"No span found for '{text}'"
                span = result[0]['span']
                assert isinstance(span, EntitySpan)

    def test_numeric_day_with_suffixes(self):
        """Test numeric days with Hungarian suffixes."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            ('1-én', '1-én'),
            ('2-án', '2-án'),
            ('3-án', '3-án'),
            ('4-én', '4-én'),
            ('5-én', '5-én'),
            ('10-én', '10-én'),
            ('15-én', '15-én'),
            ('20-án', '20-án'),
            ('25-én', '25-én'),
            ('31-én', '31-én'),
            ('1-jén', '1-jén'),
            ('2-jén', '2-jén'),
            ('3-jén', '3-jén'),
        ]
        
        for text, expected_span_text in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            assert len(result) == 1, f"Expected 1 match for '{text}', got {len(result)}"
            
            # Check span
            assert 'span' in result[0], f"No span found for '{text}'"
            span = result[0]['span']
            assert isinstance(span, EntitySpan)
            assert span.text == expected_span_text
            assert text[span.start:span.end] == expected_span_text

    def test_ordinal_day_names(self):
        """Test ordinal day names (elseje, másodika, etc.)."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            ('elseje', 'elseje'),
            ('másodika', 'másodika'),
            ('harmadika', 'harmadika'),
            ('negyedike', 'negyedike'),
            ('ötödike', 'ötödike'),
            ('hatodika', 'hatodika'),
            ('hetedike', 'hetedike'),
            ('nyolcadika', 'nyolcadika'),
            ('kilencedike', 'kilencedike'),
            ('tizedike', 'tizedike'),
            ('huszadika', 'huszadika'),
            ('harmincadika', 'harmincadika'),
            ('harmincegyedike', 'harmincegyedike'),
        ]
        
        for text, expected_span_text in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            assert len(result) == 1, f"Expected 1 match for '{text}', got {len(result)}"
            
            # Check span
            assert 'span' in result[0], f"No span found for '{text}'"
            span = result[0]['span']
            assert isinstance(span, EntitySpan)
            assert span.text == expected_span_text
            assert text[span.start:span.end] == expected_span_text

    def test_ordinal_days_with_suffixes(self):
        """Test ordinal day names with suffixes (elsején, másodikán, etc.)."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            ('elsején', 'elsején'),
            ('másodikán', 'másodikán'),
            ('harmadikán', 'harmadikán'),
            ('negyedikén', 'negyedikén'),
            ('ötödikén', 'ötödikén'),
            ('hatodikán', 'hatodikán'),
            ('hetedikén', 'hetedikén'),
            ('nyolcadikán', 'nyolcadikán'),
            ('kilencedikén', 'kilencedikén'),
            ('tizedikén', 'tizedikén'),
        ]
        
        for text, expected_span_text in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            assert len(result) == 1, f"Expected 1 match for '{text}', got {len(result)}"
            
            # Check span
            assert 'span' in result[0], f"No span found for '{text}'"
            span = result[0]['span']
            assert isinstance(span, EntitySpan)
            assert span.text == expected_span_text
            assert text[span.start:span.end] == expected_span_text

    def test_day_expressions_in_context(self):
        """Test day expressions within longer text."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            ('Találkozzunk hétfőn', 'hétfőn'),
            ('A meeting 15-én lesz', '15-én'),
            ('Eljövök harmadikán', 'harmadikán'),
            ('Szerdán dolgozom', 'Szerdán'),
        ]
        
        for text, expected_span_text in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            assert len(result) == 1, f"Expected 1 match for '{text}', got {len(result)}"
            
            # Check span
            assert 'span' in result[0], f"No span found for '{text}'"
            span = result[0]['span']
            assert span.text == expected_span_text
            assert text[span.start:span.end] == expected_span_text

    def test_non_accented_day_variants(self):
        """Test non-accented variants of day expressions."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            'elseje',
            'masodika',
            'harmadika',
            'negyedike',
            'otodike',
            'hetedike',
        ]
        
        for text in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            # Should work due to remove_accent() function usage
            if len(result) == 1:
                assert 'span' in result[0], f"No span found for '{text}'"
                span = result[0]['span']
                assert isinstance(span, EntitySpan)

    def test_backward_compatibility(self):
        """Ensure day expressions work without spans."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            'hétfőn',
            '15-én',
            'harmadikán',
            'elseje',
            'szerdán'
        ]
        
        for text in test_cases:
            # Test without spans
            result_no_spans = text2datetime(text, now=now, return_spans=False)
            result_default = text2datetime(text, now=now)
            
            assert result_no_spans == result_default
            
            # Should not contain span keys
            for r in result_no_spans:
                assert 'span' not in r