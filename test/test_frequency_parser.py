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


@pytest.mark.parametrize("inp, exp", tf_frequencies)
def test_frequency_parser(inp, exp):
    result = parse_frequency(s=inp)
    assert result == exp
