from copy import copy
from datetime import date, timedelta, datetime
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class DateTimePartConatiner:
    value: Optional[int]
    rule: str


@dataclass
class Year(DateTimePartConatiner):
    pass


@dataclass
class Month(DateTimePartConatiner):
    pass


@dataclass
class Week(DateTimePartConatiner):
    pass


@dataclass
class Day(DateTimePartConatiner):
    pass


@dataclass
class Daypart(DateTimePartConatiner):
    pass


@dataclass
class Hour(DateTimePartConatiner):
    pass


@dataclass
class Minute(DateTimePartConatiner):
    pass


@dataclass
class Second(DateTimePartConatiner):
    pass


@dataclass
class OverrideTopWithNow(DateTimePartConatiner):
    pass


@dataclass
class OverrideBottomWithNow(DateTimePartConatiner):
    pass


@dataclass
class MinuteOffset(DateTimePartConatiner):
    """Indicates that a certain number of days need to be added to a date."""
    pass


@dataclass
class HourOffset(DateTimePartConatiner):
    """Indicates that a certain number of days need to be added to a date."""
    pass


@dataclass
class DayOffset(DateTimePartConatiner):
    """Indicates that a certain number of days need to be added to a date."""
    pass


@dataclass
class MonthOffset(DateTimePartConatiner):
    """Indicates that a certain number of months need to be added to a date."""
    pass


@dataclass
class YearOffset(DateTimePartConatiner):
    """Indicates that a certain number of months need to be added to a date."""
    pass


@dataclass
class StartDay(DateTimePartConatiner):
    pass


class EndDay(DateTimePartConatiner):
    pass


class SearchScopes(Enum):
    NOT_RESTRICTED = "not_restricted"
    PAST_SEARCH = "past_search"
    FUTURE_DAY = "future_day"


def is_year_realistic(year: int) -> bool:
    return 1900 < year < 2100


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

    nums = [
        'nulla',
        ('egy', "elseje", "elsejé"),
        ('ketto', 'ket', 'masod'),
        ('harom', 'harmad'),
        'negy',
        'ot',
        'hat',
        'het',
        'nyolc',
        'kilenc'
    ]

    for i, dec in enumerate(decs):
        if isinstance(dec, tuple):
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
        if isinstance(num, tuple):
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


def return_on_value_error(value):
    """
    When invalid dateparts are provided to the datetime library it throws a value error.
    For now, this solution is meant to address this issue. Later on we could implement our own sanity check logic.
    """
    def decorate(f):
        def applicator(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ValueError:
                return value

        return applicator

    return decorate


def get_type_if_exists(lst, type_to_filter):
    filtered_list = [val for val in lst if isinstance(val, type_to_filter)]
    if filtered_list:
        return filtered_list[0]
    else:
        return []


def is_smaller_date_or_none(dt1: datetime, dt2: datetime):
    if dt1 is None or dt2 is None:
        return True
    else:
        return dt1 <= dt2


@dataclass
class EntitySpan:
    """Character positions of a matched entity in text."""
    start: int
    end: int  
    text: str
    
    def __post_init__(self):
        if self.start < 0:
            raise ValueError(f"Span start cannot be negative: {self.start}")
        if self.end < self.start:
            raise ValueError(f"Span end ({self.end}) cannot be less than start ({self.start})")
        if len(self.text) != (self.end - self.start):
            raise ValueError(f"Text length ({len(self.text)}) doesn't match span length ({self.end - self.start})")


def aggregate_spans(spans: List[EntitySpan]) -> EntitySpan:
    """Combine multiple spans into one covering the full range."""
    if not spans:
        raise ValueError("Cannot aggregate empty span list")
    
    min_start = min(span.start for span in spans)
    max_end = max(span.end for span in spans)
    
    full_text = ""
    sorted_spans = sorted(spans, key=lambda s: s.start)
    
    if len(sorted_spans) == 1:
        return sorted_spans[0]
    
    for i, span in enumerate(sorted_spans):
        full_text += span.text
        if i < len(sorted_spans) - 1:
            next_span = sorted_spans[i + 1]
            gap_size = next_span.start - span.end
            if gap_size > 0:
                full_text += " " * gap_size
    
    return EntitySpan(start=min_start, end=max_end, text=full_text)


def adjust_span_for_offset(span: EntitySpan, offset: int) -> EntitySpan:
    """Adjust span positions by adding an offset."""
    return EntitySpan(
        start=span.start + offset,
        end=span.end + offset,
        text=span.text
    )
