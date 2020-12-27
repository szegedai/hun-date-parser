from typing import NamedTuple
from copy import copy
from datetime import date, timedelta

Year = NamedTuple('Year', [('x', int), ('rule', str)])
Month = NamedTuple('Month', [('x', int), ('rule', str)])
Week = NamedTuple('Week', [('x', int), ('rule', str)])
Day = NamedTuple('Day', [('x', int), ('rule', str)])
Daypart = NamedTuple('Daypart', [('x', int), ('rule', str)])
Hour = NamedTuple('Hour', [('x', int), ('rule', str)])
Minute = NamedTuple('Minute', [('x', int), ('rule', str)])
Second = NamedTuple('Second', [('x', int), ('rule', str)])


def remove_accent(s: str):
    mapping = {'á': 'a',
               'é': 'e',
               'í': 'i',
               'ó': 'o',
               'ú': 'u',
               'ö': 'o',
               'ü': 'u',
               'ő': 'o',
               'ű': 'u'}

    for a, b in mapping.items():
        s = s.replace(a, b)

    return s


def word_to_num(s: str):

    for w in s.split():
        if w.isdigit():
            return int(w)

    _s = '<DEL>' + remove_accent(copy(s))
    res = {'dec': -1, 'num': -1}
    missing = 0

    decs = [('tizen', 'tiz'),
            ('huszon', 'husz'),
            'harminc',
            'negyven',
            'otven',
            'hatvan',
            'hetven',
            'nyolcvan',
            'kilencven']

    nums = ['nulla', 'egy', ('ketto', 'ket'), 'harom', 'negy', 'ot', 'hat', 'het', 'nyolc', 'kilenc']

    for i, dec in enumerate(decs):
        if type(dec) == tuple:
            for syn in dec:
                if syn in _s:
                    res['dec'] = (i+1) * 10
                    _s = _s.replace(syn, '<DEL>')
                    break
        else:
            if dec in _s:
                res['dec'] = (i + 1) * 10
                _s = _s.replace(dec, '<DEL>')
                break

    if res['dec'] == -1:
        missing += 1
        res['dec'] = 0

    for i, num in enumerate(nums):
        if type(num) == tuple:
            for num_syn in num:
                if '<DEL>' + num_syn in _s or ' ' + num_syn in _s:
                    res['num'] = i
        else:
            if '<DEL>' + str(num) in _s or ' ' + str(num) in _s:
                res['num'] = i

    if res['num'] == -1:
        missing += 1
        res['num'] = 0

    if missing < 2:
        return res['dec'] + res['num']
    else:
        return -1


def num_to_word(num: int):
    assert 0 <= num < 60

    decs = ['tizen',
            'huszon',
            'harminc',
            'negyven',
            'ötven']

    nums = ['nulla', 'egy', 'kettő', 'három', 'négy', 'öt', 'hat', 'hét', 'nyolc', 'kilenc']

    if num == 0:
        return 'nulla'
    if num == 10:
        return 'tíz'
    if num == 20:
        return 'húsz'

    res = ''

    if num // 10:
        res += decs[(num // 10) - 1]

    if num % 10:
        res += nums[(num % 10)]

    return res


def monday_of_calenderweek(year, week):
    first = date(year, 1, 1)
    base = 1 if first.isocalendar()[1] == 1 else 8
    return first + timedelta(days=base - first.isocalendar()[2] + 7 * (week - 1))
