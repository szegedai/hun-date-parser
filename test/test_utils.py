from src.date_parser.utils import word_to_num, remove_accent


def test_remove_accent():
    tf = [('aáéeíiő', 'aaeeiio')]

    for inp, exp in tf:
        print(inp, exp)
        assert remove_accent(inp) == exp


def test_word_to_num():
    tf = [('egy', 1),
          ('tizenegy', 11),
          ('húsz', 20),
          ('kilencvenhat', 96),
          ('random', -1),
          ('huszonketto', 22),
          ('kilencvenkilenc', 99),
          ('nulla', 0),
          ('tiz', 10),
          ('xyz negyvenhat', 46),
          ('ötvenöt perckor', 55),
          ('55 perckor', 55),
          ('8 húsz perckor', 8),
          ('8', 8),
          ('előtt nyolcvan perccel', 80),
          ('ma reggel nyolc óra', 8)]

    for inp, exp in tf:
        assert word_to_num(inp) == exp
