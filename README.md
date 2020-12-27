<h1 align="center">Hungarian Date Parser</h1>

<p align="center">
    <i>A tool for extracting datetime intervals from Hungarian sentences and turning datetime objects into Hungarian text.</i>
</p>


<div align="center">
    <a href="https://badge.fury.io/py/hun-date-parser"><img src="https://badge.fury.io/py/hun-date-parser.svg" alt="PyPI version" height="18"></a>
    <img src="https://img.shields.io/github/stars/nsoma97/hun-date-parser" alt="Stars Badge"/>
    <img src="https://img.shields.io/github/issues/nsoma97/hun-date-parser" alt="Issues Badge"/>
    <img src="https://img.shields.io/github/license/nsoma97/hun-date-parser?color=2b9348" alt="License Badge"/>
    <img src="https://img.shields.io/github/workflow/status/nsoma97/hun-date-parser/Datetime Parser Pipeline" alt="Tests"/>
    <a href='https://coveralls.io/github/nsoma97/hun-date-parser'><img src='https://coveralls.io/repos/github/nsoma97/hun-date-parser/badge.svg' alt='Coverage Status' /></a>
</div>

<br>


Install and try the package with `pip install hun-date-parser`.

## :fire: Usage

If not specified otherwise, relative dates (eg.: tomorrow, next week, etc.) are calculated relative to the current datetime, at the time when the DatetimeExtractor is instanciated.

```python
from hun_date_parser import DatetimeExtractor

datetime_extractor = DatetimeExtractor()

datetime_extractor.parse_datetime('találkozzunk jövő kedd délután!')
# {'start_date': datetime.datetime(2020, 12, 29, 12, 0), 'end_date': datetime.datetime(2020, 12, 29, 17, 59, 59)}

datetime_extractor.parse_datetime('találkozzunk szombaton háromnegyed nyolc előtt két perccel')
# {'start_date': datetime.datetime(2020, 12, 26, 7, 43), 'end_date': datetime.datetime(2020, 12, 26, 7, 43, 59)}
```
The date parser is also capable of parsing explicit intervals from the text even when only one side of the interval is specified.
```python
datetime_extractor.parse_datetime('2020 decemberétől 2021 januárig')
# {'start_date': datetime.datetime(2020, 12, 1, 0, 0), 'end_date': datetime.datetime(2021, 1, 31, 23, 59, 59)}


datetime_extractor.parse_datetime('2020 decemberéig')
# {'start_date': None, 'end_date': datetime.datetime(2020, 12, 31, 23, 59, 59)}
```

The library is also capable of turning datetime objects into their Hungarian text representation.

```python
from datetime import datetime
from hun_date_parser import DatetimeTextualizer

datetime_textualizer = DatetimeTextualizer()

datetime_textualizer.generate_candidates()

datetime_textualizer.generate_candidates(datetime(2020, 12, 20, 18, 34), time_precision=2)
# {'date': ['ezen a héten vasárnap', '2020 december 20'],
#  'times': ['tizennyolc óra harmincnégy perc', '18:34', 'este hat óra harmincnégy perc', 'este fél 7 után 4 perccel']}
```

## :pencil: License

This project is licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) license. Feel free to use it in your own projects.

## :wrench: Contribute

Any help or feedback in further developing the library is welcome!
