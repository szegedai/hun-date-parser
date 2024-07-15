<h1 align="center">Hungarian Date Parser</h1>

<p align="center">
    <i>A tool for extracting datetime intervals from Hungarian sentences and turning datetime objects into Hungarian text.</i>
</p>


<div align="center">
    <a href="https://badge.fury.io/py/hun-date-parser"><img src="https://badge.fury.io/py/hun-date-parser.svg" alt="PyPI version" height="18"></a>
    <img src="https://img.shields.io/github/stars/nsoma97/hun-date-parser" alt="Stars Badge"/>
    <img src="https://img.shields.io/github/issues/nsoma97/hun-date-parser" alt="Issues Badge"/>
    <img src="https://img.shields.io/github/license/nsoma97/hun-date-parser?color=2b9348" alt="License Badge"/>
    <a href='https://coveralls.io/github/nsoma97/hun-date-parser'><img src='https://coveralls.io/repos/github/nsoma97/hun-date-parser/badge.svg' alt='Coverage Status' /></a>
</div>

<br>


Install and try the package with `pip install hun-date-parser`

## :fire: Usage

```python
from hun_date_parser import text2datetime
from datetime import datetime

text2datetime('találkozzunk jövő kedd délután!', now=datetime(2020, 12, 27))
# [{'start_date': datetime.datetime(2020, 12, 29, 12, 0), 'end_date': datetime.datetime(2020, 12, 29, 17, 59, 59)}]

text2datetime('találkozzunk jövő héten szombaton háromnegyed nyolc előtt két perccel', now=datetime(2020, 12, 27))
# [{'start_date': datetime.datetime(2021, 1, 2, 7, 43), 'end_date': datetime.datetime(2021, 1, 2, 7, 43, 59)}]

text2datetime('találkozzunk jövő héten szombaton este háromnegyed nyolc előtt két perccel', now=datetime(2020, 12, 27))
# [{'start_date': datetime.datetime(2021, 1, 2, 19, 43), 'end_date': datetime.datetime(2021, 1, 2, 19, 43, 59)}]
```
The date parser is also capable of parsing explicit intervals from the text even when only one side of the interval is specified.
```python
from hun_date_parser import text2datetime
from datetime import datetime

text2datetime('2020 decemberétől 2021 januárig', now=datetime(2020, 12, 27))
# [{'start_date': datetime.datetime(2020, 12, 1, 0, 0), 'end_date': datetime.datetime(2021, 1, 31, 23, 59, 59)}]

text2datetime('2021 januárig', now=datetime(2020, 12, 27))
# [{'start_date': None, 'end_date': datetime.datetime(2021, 1, 31, 23, 59, 59)}]
```

If not specified otherwise, relative dates (eg.: tomorrow, next week, etc.) are calculated relative to the current datetime, at the time when the function is called. The `now` parameter can be used for parsing relative datetimes relative to any timestamp other than the current time.

### Supported formats


Our parser implements a rule-based strategy to interpret a diverse array of date and time formats, utilizing grammatical inflection to parse intervals.

The following formats are currently supported:

#### Date Formats:
- **ISO Standard Dates**: dates formatted to the ISO 8601 standard.
  - Examples: `2020-01-15`, `2020-12-30-án`, `2020.12.29`.
- **Named Months**: months indicated by name, optionally with day numbers and/or year. Day numbers may be expressed lexically.
  - Examples: `tavaly február`, `2020 február 3`, `jövő március`, `jövő február 12-én`, `március elsején`.
- **Relative Time References**: relative days, weeks, months, or years.
  - Examples: `tegnap`, `ma`, `holnap`, `idén`, `tavaly`, `múlt héten`, `a múlt hónapban`, `idei események`.
- **Named Days of the Week**: references to specific weekdays, accounting for past, present, and future contexts.
  - Examples: `múlt vasárnap`, `kedden`, `ezen a heten hétfőn`, `jövő héten szerdán`.
- **Counted Time Frames**: expressions indicating a number of days or weeks ago or in the future.
  - Examples: `1 héttel ezelőtt`, `6 nappal ezelőtt`, `5 nap múlva`.
- **Historical Periods**: periods up to the present date, defined by days, weeks, months, or years.
  - Examples: `az előző két hétben`, `az előző két évi adatok`, `az előző 10 nap eredménye`.

#### Time Formats:
- **Digital Clock Format**: time expressed in digital clock notation.
  - Examples: `18:12-kor`, `06:45`.
- **Natural Language Time**: time described in conversational terms.
  - Examples: `este fél 8`, `reggel nyolc előtt hat perccel`, `nyolc óra nyolc perckor`, `20 óra 49 perckor`, `este negyed 8 előtt 6 perccel`.
- **Abbreviated Time Formats**: certain abbreviated forms of time expression.
  - Examples: `16h-kor`.

#### Interval Formats:
- **Inflection-Implied Ranges**: intervals detected through grammatical inflections, indicating a start and end point.
  - Examples: `február 13-tól 17-ig`, `keddtől péntekig`, `januártól februárig`, `2020-10-12-től 2020-11-01-ig`.
- **Open-Ended Intervals**: expressions where the start or end of the interval is unspecified, using inflections to imply boundaries.
  - Examples: `keddtől`, `február elsejéig`.


### Setting search scope in case of ambiguous input

For the function `text2datetime`, the parameter `search_scope` is used to specify the desired time interval for parsing inputs.
- The default value, `SearchScopes.NOT_RESTRICTED`, does not restrict whether the scope of the search is in the past or the future.
  - For example, when Tuesday is parsed, the date for the Tuesday of the given week will be returned, without considering whether that date is in the past or the future.
- To prefer future dates in case of ambiguity, use the value `SearchScopes.FUTURE_DAY`.
  - In this case, when Tuesday is parsed, the function will return the nearest Tuesday in the future, not necessarily the current week's Tuesday.
- Similarly, to search in the past, nudging the library to prefer past dates is possible with the value `SearchScopes.PAST_SEARCH`.
  - For instance, if May is parsed by the function, with this setting, and if this year's May is still in the future, last year's May will be returned.
  - Please note that when there's no ambiguity, the function can still return future or past dates, even when a different preference is specified.

The flag `realistic_year_required` can be set in order to minimize false matches, it generally restricts year mentions to be between 1900 and 2100.
  - It defaults to true.
  - As the number 3000 is unlikely to be considered a year value in everyday contexts, it is ignored.
  - The output datetime can still be later than 2100 or earlier than 1900 with mentions of 'Counted Time Frames' (e.g., `100000 nap múlva`).

An example:
```python
from hun_date_parser import text2datetime
from datetime import datetime
from hun_date_parser.utils import SearchScopes

text2datetime('augusztus', now=datetime(2023, 6, 7), search_scope=SearchScopes.PAST_SEARCH)
# [{'start_date': datetime.datetime(2022, 8, 1, 0, 0),
#   'end_date': datetime.datetime(2022, 8, 31, 23, 59, 59)}]

text2datetime('péntek', now=datetime(2023, 6, 7), search_scope=SearchScopes.PAST_SEARCH)
# [{'start_date': datetime.datetime(2023, 6, 2, 0, 0),
#   'end_date': datetime.datetime(2023, 6, 2, 23, 59, 59)}]

text2datetime('péntek', now=datetime(2023, 6, 7), search_scope=SearchScopes.NOT_RESTRICTED)
# [{'start_date': datetime.datetime(2023, 6, 9, 0, 0),
#   'end_date': datetime.datetime(2023, 6, 9, 23, 59, 59)}]
```

### Duration Parsing

The duration parser can extract the duration in minutes from various expressions found in sentences.

#### Recognized Formats

The parser is capable of understanding a variety of duration expressions. Here are the primary formats it recognizes:

- Hour and Minute Combination:
  - Examples: `1 óra 45 perc`, `egy óra 30 perc`, `2 óra 15 perc`
- Hour Only:
  - Examples: `1 óra`, `egy óra`, `2 órát`, `3,5 óra`
- Quarter Hour Phrases:
  - Examples: `háromnegyed óra`, `egy és negyed óra`, `kettő és fél óra`


```python
from hun_date_parser import parse_duration

print(parse_duration('45 perc'))  # Output: 45

print(parse_duration('1 és negyed óra'))  # Output: 75
```

### Datetime to text

The library is also capable of turning datetime objects into their Hungarian text representation.

```python
from hun_date_parser import datetime2text
from datetime import datetime

datetime2text(datetime(2020, 12, 20, 18, 34), now=datetime(2020, 12, 27), time_precision=2)
# {'dates': ['múlt héten vasárnap', '2020 december 20'],
#  'times': ['tizennyolc óra harmincnégy perc', '18:34', 'este hat óra harmincnégy perc', 'este fél 7 után 4 perccel']}
```

## :pencil: License

This project is licensed under [MIT](https://choosealicense.com/licenses/mit/) license. Feel free to use it in your own projects.

## :wrench: Contribute

Any help or feedback in further developing the library is welcome!
