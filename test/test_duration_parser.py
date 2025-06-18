import pytest
from datetime import datetime

from hun_date_parser.duration_parser.duration_parsers import duration_parser, parse_duration
from hun_date_parser.date_parser.date_parsers import Minute


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
    ("100 órára", []),
    ("", []),
    ("  fél", []),
    ("  jövő kedd", []),
    ("délig", []),
]

@pytest.mark.parametrize("inp, exp", tf_durations)
def test_named_month(inp, exp):
    duration_dct = duration_parser(s=inp)

    assert duration_dct["date_parts"] == exp


@pytest.mark.parametrize("inp, exp", tf_durations)
def test_parse_duration(inp, exp):
    duration = parse_duration(inp)

    if not exp:
        assert duration is None
    else:
        assert duration == exp[0].value
