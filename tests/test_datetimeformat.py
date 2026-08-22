from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

import pytest

from python_intl import DateTimeFormat
from python_intl.datetimeformat import DateTimeFormatOptions

from .utils import normalize_parts_whitespace, normalize_range_whitespace

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
def test_options_to_json(options_: DateTimeFormatOptionsDictT, expected: DateTimeFormatOptionsDictT):
    options = DateTimeFormatOptions(**options_)
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


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en-US", "8/15/2026 \u2013 9/30/2026"),
        ("en-GB", "15/08/2026 \u2013 30/09/2026"),
        ("de-DE", "15.08. \u2013 30.09.2026"),
        # In Sweden there would be no whitespace next to the EN_DASH, but we normalise it before comparison
        ("sv-SE", "2026-08-15 \u2013 09-30"),
    ],
)
def test_full_numeric_date_range(locale: str, expected: str):
    datetime_start = dt.datetime(2026, 8, 15)
    datetime_end = dt.datetime(2026, 9, 30)
    formatter = DateTimeFormat(locale, {"year": "numeric", "month": "2-digit", "day": "2-digit"})
    assert normalize_range_whitespace(formatter.format_range(datetime_start, datetime_end)) == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en-US", "8/15/2025 \u2013 9/30/2026"),
        ("en-GB", "15/08/2025 \u2013 30/09/2026"),
        ("de-DE", "15.08.2025 \u2013 30.09.2026"),
        # In Sweden there would be no whitespace next to the EN_DASH, but we normalise it before comparison
        ("sv-SE", "2025-08-15 \u2013 2026-09-30"),
    ],
)
def test_full_numeric_date_range_over_year(locale: str, expected: str):
    datetime_start = dt.datetime(2025, 8, 15)
    datetime_end = dt.datetime(2026, 9, 30)
    formatter = DateTimeFormat(locale, {"year": "numeric", "month": "2-digit", "day": "2-digit"})
    assert normalize_range_whitespace(formatter.format_range(datetime_start, datetime_end)) == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        (
            "en-US",
            [
                {"type": "month", "value": "8", "source": "startRange"},
                {"type": "literal", "value": "/", "source": "startRange"},
                {"type": "day", "value": "15", "source": "startRange"},
                {"type": "literal", "value": "/", "source": "startRange"},
                {"type": "year", "value": "2026", "source": "startRange"},
                {"type": "literal", "value": " \u2013 ", "source": "shared"},
                {"type": "month", "value": "9", "source": "endRange"},
                {"type": "literal", "value": "/", "source": "endRange"},
                {"type": "day", "value": "30", "source": "endRange"},
                {"type": "literal", "value": "/", "source": "endRange"},
                {"type": "year", "value": "2026", "source": "endRange"},
            ],
        ),
        (
            "en-GB",
            [
                {"type": "day", "value": "15", "source": "startRange"},
                {"type": "literal", "value": "/", "source": "startRange"},
                {"type": "month", "value": "08", "source": "startRange"},
                {"type": "literal", "value": "/", "source": "startRange"},
                {"type": "year", "value": "2026", "source": "startRange"},
                {"type": "literal", "value": " \u2013 ", "source": "shared"},
                {"type": "day", "value": "30", "source": "endRange"},
                {"type": "literal", "value": "/", "source": "endRange"},
                {"type": "month", "value": "09", "source": "endRange"},
                {"type": "literal", "value": "/", "source": "endRange"},
                {"type": "year", "value": "2026", "source": "endRange"},
            ],
        ),
        (
            "de-DE",
            [
                {"type": "day", "value": "15", "source": "startRange"},
                {"type": "literal", "value": ".", "source": "startRange"},
                {"type": "month", "value": "08", "source": "startRange"},
                {"type": "literal", "value": ". \u2013 ", "source": "shared"},
                {"type": "day", "value": "30", "source": "endRange"},
                {"type": "literal", "value": ".", "source": "endRange"},
                {"type": "month", "value": "09", "source": "endRange"},
                {"type": "literal", "value": ".", "source": "shared"},
                {"type": "year", "value": "2026", "source": "shared"},
            ],
        ),
        # In Sweden there would be no whitespace next to the EN_DASH, but we normalise it before comparison
        (
            "sv-SE",
            [
                {"type": "year", "value": "2026", "source": "shared"},
                {"type": "literal", "value": "-", "source": "shared"},
                {"type": "month", "value": "08", "source": "startRange"},
                {"type": "literal", "value": "-", "source": "startRange"},
                {"type": "day", "value": "15", "source": "startRange"},
                {"type": "literal", "value": " \u2013 ", "source": "shared"},
                {"type": "month", "value": "09", "source": "endRange"},
                {"type": "literal", "value": "-", "source": "endRange"},
                {"type": "day", "value": "30", "source": "endRange"},
            ],
        ),
    ],
)
def test_full_numeric_date_range_parts(locale: str, expected: str):
    datetime_start = dt.datetime(2026, 8, 15)
    datetime_end = dt.datetime(2026, 9, 30)
    formatter = DateTimeFormat(locale, {"year": "numeric", "month": "2-digit", "day": "2-digit"})
    assert (
        normalize_parts_whitespace(
            [part.to_json() for part in formatter.format_range_to_parts(datetime_start, datetime_end)],
            for_range=True,
        )
        == expected
    )


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en-US", "August 15 \u2013 September 30, 2026"),
        ("en-GB", "15 August \u2013 30 September 2026"),
        ("de-DE", "15. August \u2013 30. September 2026"),
        # In Sweden there would be no whitespace next to the EN_DASH, but we normalise it before comparison
        ("sv-SE", "15 augusti \u2013 30 september 2026"),
    ],
)
def test_written_date_range(locale: str, expected: str):
    datetime_start = dt.datetime(2026, 8, 15)
    datetime_end = dt.datetime(2026, 9, 30)
    formatter = DateTimeFormat(locale, {"year": "numeric", "month": "long", "day": "numeric"})
    assert normalize_range_whitespace(formatter.format_range(datetime_start, datetime_end)) == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en-US", "August 15, 2025 \u2013 September 30, 2026"),
        ("en-GB", "15 August 2025 \u2013 30 September 2026"),
        ("de-DE", "15. August 2025 \u2013 30. September 2026"),
        # In Sweden there would be no whitespace next to the EN_DASH, but we normalise it before comparison
        ("sv-SE", "15 augusti 2025 \u2013 30 september 2026"),
    ],
)
def test_written_date_range_over_year(locale: str, expected: str):
    datetime_start = dt.datetime(2025, 8, 15)
    datetime_end = dt.datetime(2026, 9, 30)
    formatter = DateTimeFormat(locale, {"year": "numeric", "month": "long", "day": "numeric"})
    assert normalize_range_whitespace(formatter.format_range(datetime_start, datetime_end)) == expected
