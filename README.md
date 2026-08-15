# `python-intl`

A small library using [PyICU](https://pypi.org/project/pyicu/) to provide a Python 
API similar to what the [`Intl` JavaScript API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl)
provides.

**Status:** This is very much work in progress. Currently only `Intl.DateTimeFormat`
exists and this also is not complete yet.

## `Intl.DateTimeFormat`

### Example usage

```python
from python_intl import DateTimeFormat


datetime_ = dt.datetime(2025, 8, 15)
formatter = DateTimeFormat("de-DE", {"year": "numeric", "month": "2-digit", "day": "2-digit"})
formatter.format(datetime_)  # Will output the German format: "15.08.2026"
```

## Installation

Be sure to be able to install `PyICU`, see the installation docs there:
https://gitlab.pyicu.org/main/pyicu#installing-pyicu

**Hint:** I mainly did run into issues with `pkg-config` not finding the ICU library,
setting `PKG_CONFIG_PATH` accordingly helps most of the time I guess.
