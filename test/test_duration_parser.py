import pytest
from datetime import datetime

from hun_date_parser.duration_parser.duration_parsers import duration_parser, parse_duration, DurationUnit
from hun_date_parser.utils import Minute, Hour, Day, Week, Year


tf_durations = [
    ("45 perc", [Minute(45, "duration_parser")]),
    ("45 percre ", [Minute(45, "duration_parser")]),
    ("50 perces", [Minute(50, "duration_parser")]),
    ("120 perc", [Minute(120, "duration_parser")]),
    
    ("negyed óra", [Minute(15, "duration_parser")]),
    ("negyed órát", [Minute(15, "duration_parser")]),
    ("negyed órára", [Minute(15, "duration_parser")]),
    ("negyedórára", [Minute(15, "duration_parser")]),
    ("negyedórát", [Minute(15, "duration_parser")]),
    ("negyed óráig", [Minute(15, "duration_parser")]),
    
    (" háromnegyed óra", [Minute(45, "duration_parser")]),
    ("háromnegyed órát", [Minute(45, "duration_parser")]),
    ("háromnegyed órára", [Minute(45, "duration_parser")]),
    ("háromnegyedórát", [Minute(45, "duration_parser")]),
    ("háromnegyedórára", [Minute(45, "duration_parser")]),
    ("3 negyedóra", [Minute(45, "duration_parser")]),
    ("a háromnegyedóra hosszú időtartam", [Minute(45, "duration_parser")]),
    ("a háromnegyed óra hosszú időtartam", [Minute(45, "duration_parser")]),
    ("a háromnegyed órás időtartam", [Minute(45, "duration_parser")]),

    ("másfél óra", [Minute(90, "duration_parser")]),
    ("a másfél óra hosszú időtartam", [Minute(90, "duration_parser")]),
    ("másfélóra", [Minute(90, "duration_parser")]),
    ("másfélórás", [Minute(90, "duration_parser")]),
    ("a másfélórás időtartam", [Minute(90, "duration_parser")]),
    ("másfél órára", [Minute(90, "duration_parser")]),
    ("másfél órát", [Minute(90, "duration_parser")]),
    (" másfél órát ", [Minute(90, "duration_parser")]),
    (" másfél órányi ", [Minute(90, "duration_parser")]),
    (" a parkolás másfél órán át tart ", [Minute(90, "duration_parser")]),
    (" a parkolás másfélórán át tart ", [Minute(90, "duration_parser")]),
    (" a másfél órás parkolás ", [Minute(90, "duration_parser")]),
    (" a másfél órás parkolás ", [Minute(90, "duration_parser")]),
    ("másfélórára", [Minute(90, "duration_parser")]),
    ("másfélórát", [Minute(90, "duration_parser")]),
    ("a másfélórát b", [Minute(90, "duration_parser")]),
    ("indítsd el másfélórára", [Minute(90, "duration_parser")]),
    ("indítsd el másfél órára", [Minute(90, "duration_parser")]),
    ("a másfélórás időtartam", [Minute(90, "duration_parser")]),

    
    ("25 perc", [Minute(25, "duration_parser")]),
    ("26 perc", [Minute(26, "duration_parser")]),
    ("1 óra 25 perc", [Minute(85, "duration_parser")]),
    ("1,5 óráig", [Minute(90, "duration_parser")]),
    ("2,5 óráig", [Minute(150, "duration_parser")]),
    ("1 óráig", [Minute(60, "duration_parser")]),
    ("1 és negyed óráig", [Minute(75, "duration_parser")]),
    ("1 és negyedóráig", [Minute(75, "duration_parser")]),
    ("egy és fél óráig", [Minute(90, "duration_parser")]),
    ("félóráig", [Minute(30, "duration_parser")]),
    ("eddig 3 és negyed óráig", [Minute(195, "duration_parser")]),
    ("eddig 3 es negyed oraig", [Minute(195, "duration_parser")]),
    ("eddig: 1,5 óráig", [Minute(90, "duration_parser")]),
    ("eddig: 45 percre", [Minute(45, "duration_parser")]),
    ("egy óra 10 percre", [Minute(70, "duration_parser")]),
    (": egy óra 10 percre :", [Minute(70, "duration_parser")]),

    ("16 percre", [Minute(16, "duration_parser")]),
    ("99 percre", [Minute(99, "duration_parser")]),
    ("999 percre", [Minute(999, "duration_parser")]),
    ("2 óra 16 percre", [Minute(136, "duration_parser")]),

    ("3 órára", [Minute(180, "duration_parser")]),
    ("4 órára", [Minute(240, "duration_parser")]),
    ("5 órára", [Minute(300, "duration_parser")]),
    ("6 órára", [Minute(360, "duration_parser")]),
    ("10 órára", [Minute(600, "duration_parser")]),

    ("16", []),
    ("", []),
    ("  fél", []),
    ("  jövő kedd", []),
    ("délig", []),
]

tf_durations_new_os = [
    ("éves", [Minute(365 * 24 * 60, "duration_parser")]),
    ("évesét", [Minute(365 * 24 * 60, "duration_parser")]),
    ("1 éves", [Minute(365 * 24 * 60, "duration_parser")]),
    ("egy éves", [Minute(365 * 24 * 60, "duration_parser")]),
    ("2 éves", [Minute(2 * 365 * 24 * 60, "duration_parser")]),
    
    ("1 hetes", [Minute(7 * 24 * 60, "duration_parser")]),
    ("egy hetes", [Minute(7 * 24 * 60, "duration_parser")]),
    ("1 heteset", [Minute(7 * 24 * 60, "duration_parser")]),
    ("1 hetest", [Minute(7 * 24 * 60, "duration_parser")]),
    ("2 hetest", [Minute(2 * 7 * 24 * 60, "duration_parser")]),
    ("kéthetes", [Minute(2 * 7 * 24 * 60, "duration_parser")]),
    ("kéthetesét", [Minute(2 * 7 * 24 * 60, "duration_parser")]),
    ("3 hetes", [Minute(3 * 7 * 24 * 60, "duration_parser")]),
    
    ("10 napos", [Minute(10 * 24 * 60, "duration_parser")]),
    ("10 naposát", [Minute(10 * 24 * 60, "duration_parser")]),
    ("30 napos", [Minute(30 * 24 * 60, "duration_parser")]),
    ("30 naposát", [Minute(30 * 24 * 60, "duration_parser")]),
    ("egy napos", [Minute(24 * 60, "duration_parser")]),
    ("egynapos", [Minute(24 * 60, "duration_parser")]),
    ("harmincnapos", [Minute(30 * 24 * 60, "duration_parser")]),
    ("5 napos", [Minute(5 * 24 * 60, "duration_parser")]),
    
    ("24 órás", [Minute(24 * 60, "duration_parser")]),
    ("24 órását", [Minute(24 * 60, "duration_parser")]),
    ("1 órás", [Minute(60, "duration_parser")]),
    ("egy órás", [Minute(60, "duration_parser")]),
    ("8 órás", [Minute(8 * 60, "duration_parser")]),
]

tf_durations_new_ra = [
    ("évre", [Minute(365 * 24 * 60, "duration_parser")]),
    ("egy évre", [Minute(365 * 24 * 60, "duration_parser")]),
    ("1 évre", [Minute(365 * 24 * 60, "duration_parser")]),
    ("teljes évre", [Minute(365 * 24 * 60, "duration_parser")]),
    ("2 évre", [Minute(2 * 365 * 24 * 60, "duration_parser")]),
    
    ("1 hétre", [Minute(7 * 24 * 60, "duration_parser")]),
    ("egy hétre", [Minute(7 * 24 * 60, "duration_parser")]),
    ("2 hétre", [Minute(2 * 7 * 24 * 60, "duration_parser")]),
    ("két hétre", [Minute(2 * 7 * 24 * 60, "duration_parser")]),
    ("3 hétre", [Minute(3 * 7 * 24 * 60, "duration_parser")]),
    
    ("1 napra", [Minute(24 * 60, "duration_parser")]),
    ("egy napra", [Minute(24 * 60, "duration_parser")]),
    ("7 napra", [Minute(7 * 24 * 60, "duration_parser")]),
    ("30 napra", [Minute(30 * 24 * 60, "duration_parser")]),
    ("31 napra", [Minute(31 * 24 * 60, "duration_parser")]),
    ("harminc napra", [Minute(30 * 24 * 60, "duration_parser")]),
    ("365 napra", [Minute(365 * 24 * 60, "duration_parser")]),
    
    ("24 órára", [Minute(24 * 60, "duration_parser")]),
    ("1 órára", [Minute(60, "duration_parser")]),
    ("egy órára", [Minute(60, "duration_parser")]),
    ("8 órára", [Minute(8 * 60, "duration_parser")]),
]

@pytest.mark.parametrize("inp, exp", tf_durations)
def test_named_month(inp, exp):
    duration_dct = duration_parser(s=inp)

    assert duration_dct["date_parts"] == exp


@pytest.mark.parametrize("inp, exp", tf_durations_new_os)
def test_duration_os_patterns(inp, exp):
    """Test -os/-as suffix patterns"""
    duration_dct = duration_parser(s=inp)
    assert duration_dct["date_parts"] == exp


@pytest.mark.parametrize("inp, exp", tf_durations_new_ra)
def test_duration_ra_patterns(inp, exp):
    """Test -ra/-re suffix patterns"""
    duration_dct = duration_parser(s=inp)
    assert duration_dct["date_parts"] == exp


@pytest.mark.parametrize("inp, exp", tf_durations)
def test_parse_duration(inp, exp):
    duration = parse_duration(inp)

    if not exp:
        assert duration is None
    else:
        assert duration == exp[0].value


tf_preferred_units = [
    ("éves", DurationUnit.YEARS, 1, "year"),
    ("2 éves", DurationUnit.YEARS, 2, "year"),
    ("évre", DurationUnit.YEARS, 1, "year"),
    ("teljes évre", DurationUnit.YEARS, 1, "year"),
    
    ("1 hetes", DurationUnit.WEEKS, 1, "week"),
    ("egyhetes", DurationUnit.WEEKS, 1, "week"),
    ("egy hetes", DurationUnit.WEEKS, 1, "week"),
    ("kéthetes", DurationUnit.WEEKS, 2, "week"),
    ("két hetes", DurationUnit.WEEKS, 2, "week"),
    ("2 hétre", DurationUnit.WEEKS, 2, "week"),
    
    ("10 napos", DurationUnit.DAYS, 10, "day"),
    ("30 napra", DurationUnit.DAYS, 30, "day"),
    ("365 napra", DurationUnit.DAYS, 365, "day"),
    
    ("24 órás", DurationUnit.HOURS, 24, "hour"),
    ("8 órára", DurationUnit.HOURS, 8, "hour"),
    ("3 órára", DurationUnit.HOURS, 3, "hour"),
    
    ("45 perc", DurationUnit.MINUTES, 45, "minute"),
    ("negyed óra", DurationUnit.MINUTES, 15, "minute"),
]


@pytest.mark.parametrize("inp, expected_preferred_unit, expected_value, expected_unit", tf_preferred_units)
def test_duration_preferred_units(inp, expected_preferred_unit, expected_value, expected_unit):
    """Test that preferred units are correctly identified"""
    result = parse_duration(inp, return_preferred_unit=True)
    
    assert result is not None
    assert result["preferred_unit"] == expected_preferred_unit.value
    assert result["value"] == expected_value
    assert result["unit"] == expected_unit
    assert "minutes" in result  # Should always include minutes for compatibility


def test_duration_backward_compatibility():
    """Test that existing functionality still works without preferred_unit parameter"""
    assert parse_duration("45 perc") == 45
    assert parse_duration("2 óra") == 120
    assert parse_duration("negyed óra") == 15
    assert parse_duration("24 órás") == 24 * 60
    assert parse_duration("1 napra") == 24 * 60
    assert parse_duration("1 hétre") == 7 * 24 * 60
    assert parse_duration("invalid") is None
    assert parse_duration("") is None


def test_duration_preferred_unit_detailed():
    """Test detailed preferred unit functionality"""
    result = parse_duration("2 évre", return_preferred_unit=True)
    expected_minutes = 2 * 365 * 24 * 60
    assert result["value"] == 2
    assert result["unit"] == "year"
    assert result["preferred_unit"] == "years"
    assert result["minutes"] == expected_minutes
    
    result = parse_duration("30 napos", return_preferred_unit=True)
    expected_minutes = 30 * 24 * 60
    assert result["value"] == 30
    assert result["unit"] == "day"
    assert result["preferred_unit"] == "days"
    assert result["minutes"] == expected_minutes
    
    result = parse_duration("45 perc", return_preferred_unit=True)
    assert result["value"] == 45
    assert result["unit"] == "minute"
    assert result["preferred_unit"] == "minutes"
    assert result["minutes"] == 45
