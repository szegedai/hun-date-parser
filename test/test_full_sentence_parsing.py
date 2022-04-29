import pytest
from datetime import datetime
from hun_date_parser import text2datetime


scenarios = [
    ('A legalacsonyabb éjszakai hőmérséklet általában 3 és 8 fok között várható.',
     [{'start_date': datetime(2022, 4, 28, 22), 'end_date': datetime(2022, 4, 29, 2, 59, 59)}]),  # éjszaka
    ('A fagyzugos részeken gyenge fagy előfordulhat.', []),
    ('A legmagasabb nappali hőmérséklet pénteken 17 és 21 fok között alakul.',
     [{'start_date': datetime(2022, 4, 29), 'end_date': datetime(2022, 4, 29, 23, 59, 59)}]),  # péntek
    ('Holnap délután esni fog, de szombaton már valószínüleg nem.',
     [{'start_date': datetime(2022, 4, 29, 12), 'end_date': datetime(2022, 4, 29, 18, 59, 59)},
      {'start_date': datetime(2022, 4, 30), 'end_date': datetime(2022, 4, 30, 23, 59, 59)}]),  # péntek du., szombat
    ('Az APT 28 a világ egyik legismertebb és legaktívabb állami hekkercsoportja, a 2016-os amerikai elnökválasztási kampány megzavarásáért is őket teszik felelőssé (az APT 29 vagy Cozy Bear nevű csoport mellett, amely egy másik orosz hírszerzőszolgálathoz, az FSZB-hez köthető).',
     [{'start_date': datetime(2016, 1, 1), 'end_date': datetime(2016, 12, 31, 23, 59, 59)}]),  # 2016
    ('Megsokasodtak mostanában a bombariadók Magyarországon, itt írtunk arról, hogy múlt héten az ország több városában, budapesti és vidéki plázákat zártak le, valamint a Szépművészeti Múzeumot is kiürítették.',
     [{'start_date': datetime(2022, 4, 18), 'end_date': datetime(2022, 4, 24, 23, 59, 59)}]),  # múlt héten
    ('Kedden újabb 1 százalékponttal 5,4 százalékra emelte a jegybanki alapkamat mértékét a nemzeti bank monetáris tanácsa.',
     [{'start_date': datetime(2022, 4, 26), 'end_date': datetime(2022, 4, 26, 23, 59, 59)}]),  # kedden
    ('Beismerte egy pécsi bankfiók kirablását a rendőr, akit szerdán vettek őrizetbe – közölte a Központi Nyomozó Főügyészség csütörtökön az MTI-vel.',
     [{'start_date': datetime(2022, 4, 27), 'end_date': datetime(2022, 4, 27, 23, 59, 59)}]),  # szerdán
    ('A Wayback Machine archívumában a 2021. decemberi verzió a legkorábbi, amikor már árulták, az időben visszafelé következő mentés 2018-as, ott még nem.',
     [{'start_date': datetime(2021, 12, 1), 'end_date': datetime(2021, 12, 31, 23, 59, 59)},
      {'start_date': datetime(2018, 1, 1), 'end_date': datetime(2018, 12, 31, 23, 59, 59)}]),
]


@pytest.mark.parametrize("inp_txt, resp", scenarios)
def test_datetime_extractor(inp_txt, resp):
    now = datetime(2022, 4, 28)
    parsed_date = text2datetime(inp_txt, now=now)

    assert parsed_date == resp
