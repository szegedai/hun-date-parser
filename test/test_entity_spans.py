import pytest
from datetime import datetime

from hun_date_parser.utils import EntitySpan
from hun_date_parser.date_parser.date_parsers import match_relative_day
from hun_date_parser import text2datetime, text2date, text2time


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


class TestMainAPISpanIntegration:
    
    def test_text2datetime_with_spans(self):
        now = datetime(2020, 10, 1)
        result = text2datetime("ma", now, return_spans=True)
        
        assert len(result) == 1
        assert 'span' in result[0]
        
        span = result[0]['span']
        assert isinstance(span, EntitySpan)
        assert span.start == 0
        assert span.end == 2
        assert span.text == "ma"
        
    def test_text2datetime_without_spans_backward_compatibility(self):
        now = datetime(2020, 10, 1)
        result = text2datetime("ma", now, return_spans=False)
        
        assert len(result) == 1
        assert 'span' not in result[0]
        assert 'start_date' in result[0]
        assert 'end_date' in result[0]
        
    def test_text2date_with_spans(self):
        now = datetime(2020, 10, 1)
        result = text2date("ma", now, return_spans=True)
        
        assert len(result) == 1
        assert 'span' in result[0]
        
        span = result[0]['span']
        assert span.text == "ma"
        
    def test_text2time_with_spans(self):
        now = datetime(2020, 10, 1)
        result = text2time("ma reggel", now, return_spans=True)
        
        assert len(result) == 1
        assert 'span' in result[0]
        
        span = result[0]['span']
        assert "ma" in span.text
        
    def test_span_positioning_in_longer_sentence(self):
        now = datetime(2020, 10, 1)
        text = "Találkozzunk ma délben a parkban"
        result = text2datetime(text, now, return_spans=True)
        
        assert len(result) == 1
        span = result[0]['span']
        assert span.start == 13
        assert span.end == 15
        assert span.text == "ma"
        assert text[span.start:span.end] == span.text
        
    def test_multiple_temporal_expressions(self):
        now = datetime(2020, 10, 1)
        text = "ma reggel vagy holnap"
        result = text2datetime(text, now, return_spans=True)
        
        assert len(result) == 2
        
        # Should have spans for each temporal expression
        assert 'span' in result[0]
        assert 'span' in result[1]
        
        # Check span texts contain the temporal expressions
        span_texts = [r['span'].text for r in result]
        assert any("ma" in text for text in span_texts)
        assert any("holnap" in text for text in span_texts)
        
    def test_time_expressions_with_spans(self):
        now = datetime(2020, 10, 1)
        
        # Test digital clock format
        result1 = text2datetime("ma 8:30", now, return_spans=True)
        assert len(result1) == 1
        assert 'span' in result1[0]
        span1 = result1[0]['span']
        assert "8:30" in span1.text
        
        # Test "most" (now)
        result2 = text2datetime("most", now, return_spans=True)
        assert len(result2) == 1
        assert 'span' in result2[0]
        span2 = result2[0]['span']
        assert span2.text == "most"
        assert span2.start == 0
        assert span2.end == 4