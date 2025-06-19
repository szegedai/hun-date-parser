import pytest
from datetime import datetime

from hun_date_parser.utils import EntitySpan
from hun_date_parser.date_parser.date_parsers import match_relative_day


class TestEntitySpanClass:
    
    def test_entity_span_creation(self):
        span = EntitySpan(start=0, end=5, text="hello")
        assert span.start == 0
        assert span.end == 5
        assert span.text == "hello"
    
    def test_entity_span_validation(self):
        EntitySpan(start=0, end=5, text="hello")
        
        with pytest.raises(ValueError):
            EntitySpan(start=-1, end=5, text="hello")
        
        with pytest.raises(ValueError):
            EntitySpan(start=5, end=3, text="hello")
            
        with pytest.raises(ValueError):
            EntitySpan(start=0, end=5, text="hi")


class TestBasicSpanFunctionality:
    
    def test_match_relative_day_without_spans(self):
        now = datetime(2020, 10, 1)
        result = match_relative_day("ma", now)
        
        assert len(result) == 1
        assert result[0]['match'] == 'ma'
        assert 'span' not in result[0]
        
    def test_match_relative_day_with_spans(self):
        now = datetime(2020, 10, 1)
        result = match_relative_day("ma", now, return_spans=True)
        
        assert len(result) == 1
        assert result[0]['match'] == 'ma'
        assert 'span' in result[0]
        
        span = result[0]['span']
        assert isinstance(span, EntitySpan)
        assert span.start == 0
        assert span.end == 2
        assert span.text == "ma"
        
    def test_span_positioning_in_longer_text(self):
        now = datetime(2020, 10, 1)
        text = "Találkozzunk ma délben"
        result = match_relative_day(text, now, return_spans=True)
        
        assert len(result) == 1
        span = result[0]['span']
        assert span.start == 13
        assert span.end == 15
        assert span.text == "ma"
        assert text[span.start:span.end] == span.text
        
    def test_multiple_matches_in_text(self):
        now = datetime(2020, 10, 1)
        text = "ma reggel vagy holnap"
        result = match_relative_day(text, now, return_spans=True)
        
        assert len(result) == 2
        
        ma_result = next(r for r in result if 'ma' in r['match'])
        ma_span = ma_result['span']
        assert ma_span.start == 0
        assert ma_span.end == 2
        assert ma_span.text == "ma"
        
        holnap_result = next(r for r in result if 'holnap' in r['match'])
        holnap_span = holnap_result['span']
        assert holnap_span.start == 15
        assert holnap_span.end == 21
        assert holnap_span.text == "holnap"
        
    def test_different_relative_day_patterns(self):
        now = datetime(2020, 10, 1)
        
        test_cases = [
            ("holnap", "holnap"),
            ("holnapután", "holnapután"),
        ]
        
        for text, expected_match in test_cases:
            result = match_relative_day(text, now, return_spans=True)
            if result:
                matching_result = None
                for r in result:
                    if expected_match in r['match']:
                        matching_result = r
                        break
                
                assert matching_result is not None, f"Expected match '{expected_match}' not found in results"
                span = matching_result['span']
                assert span.start == 0
                assert span.text == text


class TestSpanEdgeCases:
    
    def test_no_matches_returns_empty_with_spans(self):
        now = datetime(2020, 10, 1)
        result = match_relative_day("nincs semmi", now, return_spans=True)
        assert result == []
        
    def test_whitespace_handling(self):
        now = datetime(2020, 10, 1)
        text = "   ma   "
        result = match_relative_day(text, now, return_spans=True)
        
        assert len(result) == 1
        span = result[0]['span']
        assert span.start == 3
        assert span.end == 5
        assert span.text == "ma"