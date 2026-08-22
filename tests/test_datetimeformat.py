from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

import pytest

from python_intl import DateTimeFormat
from python_intl.datetimeformat import DateTimeFormatOptions

if TYPE_CHECKING:
    from python_intl.datetimeformat import DateTimeFormatOptionsDictT


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (
            {"year": "numeric", "month": "2-digit", "day": "2-digit"},
            {"year": "numeric", "month": "2-digit", "day": "2-digit"},
        ),
        (
            {"hour": "numeric", "minute": "numeric", "day_period": "short"},
            {"hour": "numeric", "minute": "numeric", "dayPeriod": "short"},
        ),
        (
            {"hour": "numeric", "minute": "numeric", "time_zone_name": "short_offset"},
            {"hour": "numeric", "minute": "numeric", "timeZoneName": "shortOffset"},
        ),
    ],
)
def test_options_to_json(options: DateTimeFormatOptionsDictT, expected: DateTimeFormatOptionsDictT):
    options = DateTimeFormatOptions(**options)
    assert options.to_json() == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en-US", "08/15/2026"),
        ("en-GB", "15/08/2026"),
        ("de-DE", "15.08.2026"),
        ("sv-SE", "2026-08-15"),
    ],
)
def test_full_numeric_date(locale: str, expected: str):
    datetime_ = dt.datetime(2026, 8, 15)
    formatter = DateTimeFormat(locale, {"year": "numeric", "month": "2-digit", "day": "2-digit"})
    assert formatter.format(datetime_) == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en-US", [("month", "08"), ("literal", "/"), ("day", "15"), ("literal", "/"), ("year", "2026")]),
        ("en-GB", [("day", "15"), ("literal", "/"), ("month", "08"), ("literal", "/"), ("year", "2026")]),
        ("de-DE", [("day", "15"), ("literal", "."), ("month", "08"), ("literal", "."), ("year", "2026")]),
        ("sv-SE", [("year", "2026"), ("literal", "-"), ("month", "08"), ("literal", "-"), ("day", "15")]),
    ],
)
def test_full_numeric_date_parts(locale: str, expected: str):
    datetime_ = dt.datetime(2026, 8, 15)
    formatter = DateTimeFormat(locale, {"year": "numeric", "month": "2-digit", "day": "2-digit"})
    assert [(part.type, part.value) for part in formatter.format_to_parts(datetime_)] == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en-US", "August 15, 2026"),
        ("en-GB", "15 August 2026"),
        ("de-DE", "15. August 2026"),
        ("sv-SE", "15 augusti 2026"),
    ],
)
def test_written_date(locale: str, expected: str):
    datetime_ = dt.datetime(2026, 8, 15)
    formatter = DateTimeFormat(locale, {"year": "numeric", "month": "long", "day": "numeric"})
    assert formatter.format(datetime_) == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en-US", [("month", "August"), ("literal", " "), ("day", "15"), ("literal", ", "), ("year", "2026")]),
        ("en-GB", [("day", "15"), ("literal", " "), ("month", "August"), ("literal", " "), ("year", "2026")]),
        ("de-DE", [("day", "15"), ("literal", ". "), ("month", "August"), ("literal", " "), ("year", "2026")]),
        ("sv-SE", [("day", "15"), ("literal", " "), ("month", "augusti"), ("literal", " "), ("year", "2026")]),
    ],
)
def test_written_date_parts(locale: str, expected: str):
    datetime_ = dt.datetime(2026, 8, 15)
    formatter = DateTimeFormat(locale, {"year": "numeric", "month": "long", "day": "numeric"})
    assert [(part.type, part.value) for part in formatter.format_to_parts(datetime_)] == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en-US", "Saturday, August 15"),
        ("en-GB", "Saturday 15 August"),
        ("de-DE", "Samstag, 15. August"),
        ("sv-SE", "lördag 15 augusti"),
    ],
)
def test_written_day_and_date(locale: str, expected: str):
    datetime_ = dt.datetime(2026, 8, 15)
    formatter = DateTimeFormat(locale, {"month": "long", "day": "numeric", "weekday": "long"})
    assert formatter.format(datetime_) == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        (
            "en-US",
            [
                ("weekday", "Saturday"),
                ("literal", ", "),
                ("month", "August"),
                ("literal", " "),
                ("day", "15"),
            ],
        ),
        (
            "en-GB",
            [
                ("weekday", "Saturday"),
                ("literal", " "),
                ("day", "15"),
                ("literal", " "),
                ("month", "August"),
            ],
        ),
        (
            "de-DE",
            [
                ("weekday", "Samstag"),
                ("literal", ", "),
                ("day", "15"),
                ("literal", ". "),
                ("month", "August"),
            ],
        ),
        (
            "sv-SE",
            [
                ("weekday", "lördag"),
                ("literal", " "),
                ("day", "15"),
                ("literal", " "),
                ("month", "augusti"),
            ],
        ),
    ],
)
def test_written_day_and_date_parts(locale: str, expected: str):
    datetime_ = dt.datetime(2026, 8, 15)
    formatter = DateTimeFormat(locale, {"month": "long", "day": "numeric", "weekday": "long"})
    assert [(part.type, part.value) for part in formatter.format_to_parts(datetime_)] == expected
