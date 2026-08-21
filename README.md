# `python-intl`

A small library using [PyICU](https://pypi.org/project/pyicu/) to provide a Python 
API similar to what the [`Intl` JavaScript API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl)
provides. It is not meant to fully behave the same, but instead be close enough so
the "same" code works on JavaScript and Python, with similar results.

**Status:** This is very much work in progress.

**Note:** There are a lot of tests running the Python implementation against the
JavaScript one and comparing the results. In general things should be pretty
stable there. Still there are some cases with known differences. Also note
that results depend on the ICU version you have installed on your machine.

## General notes about the Python adaption

All names will be using the Python style rules. This means instead of 
`formatToParts` a method will be called `format_to_parts`. Also a dictionary
key like `dayPeriod` will be named `day_period`. Python uses snake case, let's
stick to this.

Instead of passing around undefined objects like in JavaScript we want to use
well defined and typed dataclasses. This for example is true for the
`Intl.DateTimeFormat` format options, you can use `DateTimeFormatOptions` as
a clean representation of those. Using a dictionary (which behaves the most
like those JavaScript objects) is still fine and will automatically converted,
as seen in the examples here.

Many objects like for example the `DateTimeFormatOptions` provide methods to
convert their Python representation to a JavaScript compatible JSON format
by returning a `dict` using the JavaScript naming. You can use the `to_json`
method for this.

For example:
```python
import python_intl as Intl

Intl.DateTimeFormatOptions(time_zone_name="short_offset").to_json()
# Will return: {'timeZoneName': 'shortOffset'}
```

## Available `Intl` classes

### `Intl.DateTimeFormat`

#### Example usage

```python
import datetime as dt
import python_intl as Intl

# Format a datetime
datetime = dt.datetime(2026, 8, 15)
formatter = Intl.DateTimeFormat("de-DE", {"year": "numeric", "month": "2-digit", "day": "2-digit"})
formatter.format(datetime)
# Result = "15.08.2026"

# Format a datetime range
datetime_till = dt.datetime(2026, 9, 7)
formatter.format_range(datetime, datetime_till)
# Result = "15.08. – 07.09.2026"
```

#### Compatibility

| Method                              | Status | Python name                            |
| ----------------------------------- | :----: | -------------------------------------- |
| `DateTimeFormat.format`             | ✅     |                                        |
| `DateTimeFormat.formatToParts`      | ✅     | `DateTimeFormat.format_to_parts`       |
| `DateTimeFormat.supportedLocalesOf` | ❌     |                                        |
| `DateTimeFormat.formatRange`        | ✅     | `DateTimeFormat.format_range`          |
| `DateTimeFormat.formatRangeToParts` | ✅     | `DateTimeFormat.format_range_to_parts` |
| `DateTimeFormat.resolvedOptions`    | ❌     |                                        |

### `Intl.Collator`

#### Compatibility

| Method             | Status | Python name |
| ------------------ | :----: | ----------- |
| `Collator.compare` | ✅     |             |

**Note:** Not all options are currently supported.

## Installation

Be sure to be able to install `PyICU`, see the installation docs there:
https://gitlab.pyicu.org/main/pyicu#installing-pyicu

**Hint:** I mainly did run into issues with `pkg-config` not finding the ICU library,
setting `PKG_CONFIG_PATH` accordingly helps most of the time I guess.

When this is done you should be able to install `python-intl` using any package
manager, like `pip install python-intl` or `uv add python-intl`.
