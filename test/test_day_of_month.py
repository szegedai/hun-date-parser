import pytest
from datetime import datetime

from hun_date_parser.date_parser.date_parsers import match_day_of_month
from hun_date_parser.date_parser.date_parsers import Day


tf_days_of_month = [
    ("1-én", [[Day(1, "day_of_month")]]),
    ("1-jén", [[Day(1, "day_of_month")]]),
    ("1-jei", [[Day(1, "day_of_month")]]),
    ("2-a", [[Day(2, "day_of_month")]]),
    ("2-án", [[Day(2, "day_of_month")]]),
    ("2-i", [[Day(2, "day_of_month")]]),
    ("2-ai", [[Day(2, "day_of_month")]]),
    ("3-át", [[Day(3, "day_of_month")]]),
    ("3-án", [[Day(3, "day_of_month")]]),
    ("4-e", [[Day(4, "day_of_month")]]),
    ("4-én", [[Day(4, "day_of_month")]]),
    ("5-én", [[Day(5, "day_of_month")]]),
    ("6-án", [[Day(6, "day_of_month")]]),
    ("7-én", [[Day(7, "day_of_month")]]),
    ("8-án", [[Day(8, "day_of_month")]]),
    ("9-én", [[Day(9, "day_of_month")]]),
    ("10-én", [[Day(10, "day_of_month")]]),
    ("11-én", [[Day(11, "day_of_month")]]),
    ("12-én", [[Day(12, "day_of_month")]]),
    ("13-án", [[Day(13, "day_of_month")]]),
    ("14-én", [[Day(14, "day_of_month")]]),
    ("15-én", [[Day(15, "day_of_month")]]),
    ("16-án", [[Day(16, "day_of_month")]]),
    ("17-én", [[Day(17, "day_of_month")]]),
    ("18-án", [[Day(18, "day_of_month")]]),
    ("19-én", [[Day(19, "day_of_month")]]),
    ("20-án", [[Day(20, "day_of_month")]]),
    ("21-én", [[Day(21, "day_of_month")]]),
    ("22-én", [[Day(22, "day_of_month")]]),
    ("23-án", [[Day(23, "day_of_month")]]),
    ("24-én", [[Day(24, "day_of_month")]]),
    ("25-én", [[Day(25, "day_of_month")]]),
    ("26-án", [[Day(26, "day_of_month")]]),
    ("27-én", [[Day(27, "day_of_month")]]),
    ("28-án", [[Day(28, "day_of_month")]]),
    ("29-én", [[Day(29, "day_of_month")]]),
    ("30-án", [[Day(30, "day_of_month")]]),
    ("31-én", [[Day(31, "day_of_month")]]),
    
    ("3-ától", [[Day(3, "day_of_month")]]),
    ("5-étől", [[Day(5, "day_of_month")]]),
    ("10-étől", [[Day(10, "day_of_month")]]),
    ("15-étől", [[Day(15, "day_of_month")]]),
    ("20-ától", [[Day(20, "day_of_month")]]),
    
    ("3-áig", [[Day(3, "day_of_month")]]),
    ("5-éig", [[Day(5, "day_of_month")]]),
    ("10-éig", [[Day(10, "day_of_month")]]),
    ("15-éig", [[Day(15, "day_of_month")]]),
    ("20-áig", [[Day(20, "day_of_month")]]),
    
    ("elsején", [[Day(1, "day_of_month")]]),
    ("elsejétől", [[Day(1, "day_of_month")]]),
    ("elsejéig", [[Day(1, "day_of_month")]]),
    ("elseje", [[Day(1, "day_of_month")]]),
    ("elsejéig", [[Day(1, "day_of_month")]]),
    ("elsejei", [[Day(1, "day_of_month")]]),

    ("másodikán", [[Day(2, "day_of_month")]]),
    ("másodika", [[Day(2, "day_of_month")]]),
    ("másodikáig", [[Day(2, "day_of_month")]]),
    
    ("harmadikán", [[Day(3, "day_of_month")]]),
    ("harmadika", [[Day(3, "day_of_month")]]),
    
    ("negyedikén", [[Day(4, "day_of_month")]]),
    ("negyedike", [[Day(4, "day_of_month")]]),
    
    ("ötödikén", [[Day(5, "day_of_month")]]),
    ("ötödike", [[Day(5, "day_of_month")]]),
    
    ("hatodikán", [[Day(6, "day_of_month")]]),
    ("hatodika", [[Day(6, "day_of_month")]]),
    
    ("hetedikén", [[Day(7, "day_of_month")]]),
    ("hetedike", [[Day(7, "day_of_month")]]),
    
    ("nyolcadikán", [[Day(8, "day_of_month")]]),
    ("nyolcadikától", [[Day(8, "day_of_month")]]),
    ("nyolcadika", [[Day(8, "day_of_month")]]),
    
    ("kilencedikén", [[Day(9, "day_of_month")]]),
    ("kilencedike", [[Day(9, "day_of_month")]]),
    
    ("tizedikén", [[Day(10, "day_of_month")]]),
    ("tizedike", [[Day(10, "day_of_month")]]),
    
    ("tizenegyedikén", [[Day(11, "day_of_month")]]),
    ("tizenegyedike", [[Day(11, "day_of_month")]]),
    
    ("tizenkettedikén", [[Day(12, "day_of_month")]]),
    ("tizenkettedike", [[Day(12, "day_of_month")]]),
    
    ("tizenharmadikán", [[Day(13, "day_of_month")]]),
    ("tizenharmadika", [[Day(13, "day_of_month")]]),
    
    ("tizennegyedikén", [[Day(14, "day_of_month")]]),
    ("tizennegyedikétől", [[Day(14, "day_of_month")]]),
    ("tizennegyedike", [[Day(14, "day_of_month")]]),
    
    ("tizenötödikén", [[Day(15, "day_of_month")]]),
    ("tizenötödike", [[Day(15, "day_of_month")]]),
    
    ("tizenhatodikán", [[Day(16, "day_of_month")]]),
    ("tizenhatodika", [[Day(16, "day_of_month")]]),
    
    ("tizenhetedikén", [[Day(17, "day_of_month")]]),
    ("tizenhetedike", [[Day(17, "day_of_month")]]),
    
    ("tizennyolcadikán", [[Day(18, "day_of_month")]]),
    ("tizennyolcadika", [[Day(18, "day_of_month")]]),
    
    ("tizenkilencedikén", [[Day(19, "day_of_month")]]),
    ("tizenkilencedike", [[Day(19, "day_of_month")]]),
    
    ("huszadikán", [[Day(20, "day_of_month")]]),
    ("huszadika", [[Day(20, "day_of_month")]]),
    
    ("huszonegyedikén", [[Day(21, "day_of_month")]]),
    ("huszonegyedike", [[Day(21, "day_of_month")]]),
    
    ("huszonkettedikén", [[Day(22, "day_of_month")]]),
    ("huszonkettedike", [[Day(22, "day_of_month")]]),
    
    ("huszonharmadikán", [[Day(23, "day_of_month")]]),
    ("huszonharmadika", [[Day(23, "day_of_month")]]),
    
    ("huszonnegyedikén", [[Day(24, "day_of_month")]]),
    ("huszonnegyedike", [[Day(24, "day_of_month")]]),
    
    ("huszonötödikén", [[Day(25, "day_of_month")]]),
    ("huszonötödike", [[Day(25, "day_of_month")]]),
    
    ("huszonhatodikán", [[Day(26, "day_of_month")]]),
    ("huszonhatodika", [[Day(26, "day_of_month")]]),
    
    ("huszonhetedikén", [[Day(27, "day_of_month")]]),
    ("huszonhetedike", [[Day(27, "day_of_month")]]),
    
    ("huszonnyolcadikán", [[Day(28, "day_of_month")]]),
    ("huszonnyolcadika", [[Day(28, "day_of_month")]]),
    
    ("huszonkilencedikén", [[Day(29, "day_of_month")]]),
    ("huszonkilencedike", [[Day(29, "day_of_month")]]),
    
    ("harmincadikán", [[Day(30, "day_of_month")]]),
    ("harmincadika", [[Day(30, "day_of_month")]]),
    
    ("harmincegyedikén", [[Day(31, "day_of_month")]]),
    ("harmincegyedike", [[Day(31, "day_of_month")]]),
    
    ("10-ei", [[Day(10, "day_of_month")]]),
    ("10-étől", [[Day(10, "day_of_month")]]),
    ("10-eig", [[Day(10, "day_of_month")]]),
    ("10-ekor", [[Day(10, "day_of_month")]]),
    
    ("találkozzunk 5-én", [[Day(5, "day_of_month")]]),
    ("a program elsején indul", [[Day(1, "day_of_month")]]),
    ("már 15-én odaérünk", [[Day(15, "day_of_month")]]),
    ("21-én reggel 8-kor", [[Day(21, "day_of_month")]]),
    ("a határidő 25-éig", [[Day(25, "day_of_month")]]),
    ("10-étől kezdődik", [[Day(10, "day_of_month")]]),
    ("a rendezvény huszonötödikén lesz", [[Day(25, "day_of_month")]]),
    ("a szerződés harmincegyedike után lép életbe", [[Day(31, "day_of_month")]]),
    
    ("", []),
    ("nincs dátum", []),
    ("32-én", []),
    ("nulladikán", []),
    ("hónapban", []),
]


@pytest.mark.parametrize("inp, exp", tf_days_of_month)
def test_day_of_month(inp, exp):
    now = datetime(2023, 5, 20)
    
    out = match_day_of_month(inp, now)
    date_parts = []
    for e in out:
        date_parts.append(e['date_parts'])
    
    assert date_parts == exp