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


Install and try the package with `pip install hun-date-parser`

## :fire: Usage

If not specified otherwise, relative dates (eg.: tomorrow, next week, etc.) are calculated relative to the current datetime, at the time when the function is called. The `now` parameter can be used for parsing relative datetimes relative to any timestamp other than the current time.

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

For the function `text2datetime` the parameter `search_scope` is used to inform what is the desired time interval to parse the inputs.

- The default value `SearchScopes.NOT_RESTRICTED` doesn't restrict the scope of the search.
  - i.e.: when Tuesday is parsed the date for the Tuesday on the given week is going to be returned, not considering whether that given date is in the past or the future
- To prefer future dates in case of ambiguity, use the value `SearchScopes.FUTURE_DAY`
  - In this case, when Tuesday is parsed, the function will return the closest Tuesday in the future, not necessarily the current week's Tuesday.
- Similarly to search in the future, nudging the library to prefer past dates is possible with the value `SearchScopes.PAST_SEARCH`
  - For instance, given a scenario when May is parsed by the function, with this setting, if this year's May is still in the future, last year's May will be returned.
  - Please note, when there's no ambiguity, the function can still return future/past dates, even when a different preference is specified.

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
