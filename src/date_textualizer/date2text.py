from datetime import date

days = [
    ['hétfő', 'hétfőn'],
    ['kedd', 'kedden'],
    ['szerda', 'szerdán'],
    ['csütörtök', 'csütörtökön'],
    ['péntek', 'pénteken'],
    ['szombat', 'szombaton'],
    ['vasárnap']
]


def date2text(d):
    if type(d) == str:
        d = date.fromisoformat(d)

    now = date.today()
    is_day_of = lambda d: days[d.weekday()][-1]
    resp = ''

    day_diff = (d - now).days
    till_next_week = 7 - now.weekday() - 1

    if day_diff == 0:
        resp += 'ma'
    elif day_diff == 1:
        resp += 'holnap'
    elif day_diff < till_next_week:
        resp += 'ezen a héten ' + is_day_of(d)
    elif day_diff > till_next_week:
        resp += 'jövőhét ' + is_day_of(d)
    elif day_diff > till_next_week + 7 and till_next_week + 14 < day_diff:
        resp += 'két hét múlva ' + is_day_of(d)
    else:
        resp += f'ekkor: {d.year}-{d.month}-{d.day}', + is_day_of(d)

    return resp
