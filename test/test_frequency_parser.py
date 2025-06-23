import pytest
from hun_date_parser.frequency_parser.frequency_parsers import parse_frequency


tf_frequencies = [
    ("naponta", "DAILY"),
    ("hetente", "WEEKLY"),
    ("kéthetente", "FORTNIGHTLY"),
    ("havonta", "MONTHLY"),
    ("negyedévente", "QUARTERLY"),
    ("félévente", "EVERY_HALF_YEAR"),
    ("évente", "YEARLY"),
    
    ("naponta", "DAILY"),
    ("hetente", "WEEKLY"),
    ("kethetente", "FORTNIGHTLY"),
    ("havonta", "MONTHLY"),
    ("negyedevente", "QUARTERLY"),
    ("felevente", "EVERY_HALF_YEAR"),
    ("evente", "YEARLY"),

    ("heti rendszerességgel", "WEEKLY"),
    ("havi rendszerességgel", "MONTHLY"),

    ("minden nap", "DAILY"),
    ("minden héten", "WEEKLY"),
    ("minden negyedévben", "QUARTERLY"),
    ("minden félévben", "EVERY_HALF_YEAR"),
    ("minden évben", "YEARLY"),
    
    ("heti", "WEEKLY"),
    ("naponként", "DAILY"),
    ("havonként", "MONTHLY"),
    ("kétheti", "FORTNIGHTLY"),
    ("napi", "DAILY"),
    ("háromhavonta", "QUARTERLY"),
    
    ("napit", "DAILY"),
    ("hetit", "WEEKLY"),
    ("kéthetit", "FORTNIGHTLY"),
    ("havit", "MONTHLY"),
    ("évi", "YEARLY"),
    ("évit", "YEARLY"),
    
    ("az értekezletet naponta tartjuk", "DAILY"),
    ("az értekezletet napi rendszerességgel tartjuk", "DAILY"),
    ("az értekezletet minden nap megtartjuk", "DAILY"),
    ("napi értekezlet", "DAILY"),
    ("találkozzunk hetente egyszer", "WEEKLY"),
    ("a csapat kéthetente tart megbeszélést", "FORTNIGHTLY"),
    ("a fizetés havonta érkezik", "MONTHLY"),
    ("a jelentést negyedévente kell benyújtani", "QUARTERLY"),
    ("az értékelés félévente történik", "EVERY_HALF_YEAR"),
    ("ez a rendezvény évente kerül megrendezésre", "YEARLY"),
    ("napi torna ajánlott", "DAILY"),
    ("minden nap egyszer", "DAILY"),
    ("minden héten egyszer", "WEEKLY"),
    ("heti megbeszélés időpontja", "WEEKLY"),
    ("kétheti ellenőrzés szükséges", "FORTNIGHTLY"),
    ("felevente kell megújítani a szerződést", "EVERY_HALF_YEAR"),
    
    ("", None),
    ("random text", None),
    ("twice a day", None),
    ("ez a szöveg nem tartalmaz gyakoriságot", None),
]


# Test cases with exact index validation
tf_index_test_cases = [
    ("Találkozzunk hetente a parkban", "WEEKLY", 13, 20),
    ("A meetingek naponta 9-kor kezdődnek", "DAILY", 12, 19),
    ("Ez a feladat minden nap elvégzendő", "DAILY", 13, 23),
    ("A nagyprojekt havonta kerül felülvizsgálatra", "MONTHLY", 14, 21)
]


@pytest.mark.parametrize("inp, exp", tf_frequencies)
def test_frequency_parser(inp, exp):
    result = parse_frequency(s=inp)
    if exp is None:
        assert result is None
    else:
        assert result is not None
        assert result.get("frequency") == exp
        assert "start" in result
        assert "end" in result
        assert result["start"] >= 0
        assert result["end"] > result["start"]


@pytest.mark.parametrize("text, freq, start, end", tf_index_test_cases)
def test_frequency_indices(text, freq, start, end):
    """Test specific cases with exact index validation"""
    result = parse_frequency(s=text)
    assert result is not None
    assert result["frequency"] == freq
    assert result["start"] == start
    assert result["end"] == end
