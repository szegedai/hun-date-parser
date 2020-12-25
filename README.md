<h1 align="center">Hungarian Date Parser</h1>

<p align="center">
    <i>A tool for extracting datetime intervals from Hungarian sentences.</i>
</p>


<div align="center">
    <img src="https://img.shields.io/github/stars/nsoma97/hun-date-parser" alt="Stars Badge"/>
    <img src="https://img.shields.io/github/issues/nsoma97/hun-date-parse" alt="Issues Badge"/>
    <img src="https://img.shields.io/github/license/nsoma97/hun-date-parse?color=2b9348" alt="License Badge"/>
    <img src="https://img.shields.io/github/workflow/status/nsoma97/hun-date-parse/datetime-parser-cicd" alt="Tests"/>
</div>

<br>


Install and try the package with `pip install hun-date-parser`.

## Usage

If not specified otherwise, relative dates (eg.: tomorrow, next week, etc.) are calculated relative to the current datetime, at the time when the DatetimeExtractor is instanciated.

```python
from hun_date_parser import DatetimeExtractor

datetime_extractor = DatetimeExtractor()

datetime_extractor.parse_datetime('találkozzunk jövő kedd délután!')

# Output: {'start_date': datetime.datetime(2020, 12, 29, 12, 0),
#          'end_date': datetime.datetime(2020, 12, 29, 17, 59, 59)}

datetime_extractor.parse_datetime('találkozzunk szombaton háromnegyed nyolc előtt két perccel')

# Output: {'start_date': datetime.datetime(2020, 12, 26, 7, 43),
#          'end_date': datetime.datetime(2020, 12, 26, 7, 43, 59)}
```
The date parser is also capable of parsing explicit intervals from the text even when only one side of the interval is specified.
```python
datetime_extractor.parse_datetime('2020 decemberétől 2021 januárig')

# Output: {'start_date': datetime.datetime(2020, 12, 1, 0, 0),
#          'end_date': datetime.datetime(2021, 1, 31, 23, 59, 59)}


datetime_extractor.parse_datetime('2020 decemberéig')

# Output: {'start_date': None,
           'end_date': datetime.datetime(2020, 12, 31, 23, 59, 59)}
```

The library is also capable of turning datetime objects into their Hungarian text representation.

```python
from hun_date_parser import 

```


## :pencil: License

This project is licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) license.

## :man_astronaut: Contribute


