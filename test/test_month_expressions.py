import pytest
from datetime import datetime

from hun_date_parser import text2datetime, text2date
from hun_date_parser.utils import EntitySpan


class TestMonthExpressions:
    
    def test_relative_month_expressions(self):
        """Test relative month expressions with span tracking."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            ('ebben a hónapban', 2020, 12, 'ebben a hónapban'),
            ('ezen a hónapban', 2020, 12, 'ezen a hónapban'),
            ('a következő hónapban', 2021, 1, 'következő hónapban'),
            ('jövő hónapban', 2021, 1, 'jövő hónapban'),
            ('múlt hónapban', 2020, 11, 'múlt hónapban'),
            ('előző hónapban', 2020, 11, 'előző hónapban'),
        ]
        
        for text, expected_year, expected_month, expected_span_text in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            assert len(result) == 1, f"Expected 1 match for '{text}', got {len(result)}"
            
            # Check date
            start_date = result[0]['start_date']
            assert start_date.year == expected_year
            assert start_date.month == expected_month
            
            # Check span
            assert 'span' in result[0], f"No span found for '{text}'"
            span = result[0]['span']
            assert isinstance(span, EntitySpan)
            assert span.text == expected_span_text
            
            # Verify span accuracy
            if expected_span_text == text:
                assert span.start == 0
                assert span.end == len(text)
            else:
                # For cases like "a következő hónapban" where span is "következő hónapban"
                assert expected_span_text in text
                assert text[span.start:span.end] == span.text

    def test_non_accented_month_expressions(self):
        """Test non-accented variants work correctly."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            ('ebben a honapban', 2020, 12),
            ('a kovetkezo honapban', 2021, 1),
            ('mult honapban', 2020, 11),
            ('elozo honapban', 2020, 11),
        ]
        
        for text, expected_year, expected_month in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            assert len(result) == 1, f"Expected 1 match for '{text}', got {len(result)}"
            
            # Check date
            start_date = result[0]['start_date']
            assert start_date.year == expected_year
            assert start_date.month == expected_month
            
            # Check span exists
            assert 'span' in result[0], f"No span found for '{text}'"

    def test_month_names_with_spans(self):
        """Test specific month names with span tracking."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            ('január', 'január'),
            ('februárban', 'február'),
            ('márciustól', 'március'),
            ('áprilisig', 'április'),
            ('januar', 'januar'),  # non-accented should also work
        ]
        
        for text, expected_span_base in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            assert len(result) == 1, f"Expected 1 match for '{text}', got {len(result)}"
            
            # Check span
            assert 'span' in result[0], f"No span found for '{text}'"
            span = result[0]['span']
            assert isinstance(span, EntitySpan)
            
            # The span should contain the base month name
            assert expected_span_base in span.text.lower()

    def test_month_expressions_in_context(self):
        """Test month expressions within longer text."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            ('Találkozzunk ebben a hónapban', 'ebben a hónapban'),
            ('A projekt jövő hónapban indul', 'jövő hónapban'),
            ('Múlt hónapban voltam ott', 'Múlt hónapban'),
        ]
        
        for text, expected_span_text in test_cases:
            result = text2datetime(text, now=now, return_spans=True)
            
            assert len(result) == 1, f"Expected 1 match for '{text}', got {len(result)}"
            
            # Check span
            assert 'span' in result[0], f"No span found for '{text}'"
            span = result[0]['span']
            assert span.text == expected_span_text
            assert text[span.start:span.end] == expected_span_text

    def test_backward_compatibility(self):
        """Ensure month expressions work without spans."""
        now = datetime(2020, 12, 27)
        
        test_cases = [
            'ebben a hónapban',
            'jövő hónapban',
            'január',
            'februárban'
        ]
        
        for text in test_cases:
            # Test without spans
            result_no_spans = text2datetime(text, now=now, return_spans=False)
            result_default = text2datetime(text, now=now)
            
            assert result_no_spans == result_default
            assert len(result_no_spans) == 1
            
            # Should not contain span keys
            assert 'span' not in result_no_spans[0]
            assert 'start_date' in result_no_spans[0]
            assert 'end_date' in result_no_spans[0]