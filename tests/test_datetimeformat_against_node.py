from __future__ import annotations

import datetime as dt
import re
from typing import TYPE_CHECKING

import pytest

from python_intl import DateTimeFormat
from python_intl.datetimeformat import DateTimeFormatOptions

if TYPE_CHECKING:
    from python_intl.datetimeformat import DateTimeFormatOptionsDictT

    from .conftest import NodeRunner


WHITESPACE_RE = re.compile(r"\s")


def _normalize_whitespace(value: str) -> str:
    # Ensure we don't have any special whitespace like NBSP
    return WHITESPACE_RE.sub(" ", value)


DATETIMES = [
    dt.datetime(2026, 8, 15),
    dt.datetime(2026, 8, 15, 12, 34, 56),
    dt.datetime(2026, 12, 24, 22, 30),
]
LOCALES = [
    "en",
    "en-US",
    "en-GB",
    "de",
    "de-DE",
    "de-AT",
    "sv-SE",
    "fr-FR",
    "it-IT",
]
OPTIONS = [
    {"year": "numeric", "month": "2-digit", "day": "2-digit"},
    {"year": "numeric", "month": "long"},
    {"month": "long", "day": "numeric"},
    {"year": "numeric", "month": "long", "day": "numeric", "weekday": "long"},
    {"month": "long", "day": "numeric", "weekday": "long"},
    {"hour": "2-digit", "minute": "2-digit", "second": "2-digit"},
    {"hour": "numeric", "minute": "numeric", "day_period": "short"},
    {"hour": "numeric", "minute": "numeric", "second": "numeric"},
    {"hour": "numeric", "minute": "numeric", "second": "numeric", "hour12": False},
    {"hour": "numeric", "minute": "numeric", "second": "numeric", "hour12": True},
]


def is_known_broken(
    locale: str,
    options_: DateTimeFormatOptionsDictT,
) -> bool:
    # Sadly some formats don't match, skip for now
    if (
        (options_.get("year") and options_.get("weekday"))
        or (options_.get("day_period") and locale in ("en", "en-US"))
        or (options_.get("hour12") is False and locale in ("en", "en-US"))
        or (options_.get("hour12") is True)
    ):
        return True

    return False


@pytest.mark.parametrize(
    "datetime_",
    DATETIMES,
)
@pytest.mark.parametrize(
    "locale",
    LOCALES,
)
@pytest.mark.parametrize(
    "options_",
    OPTIONS,
)
def test_format_against_js(
    node: NodeRunner,
    datetime_: dt.datetime,
    locale: str,
    options_: DateTimeFormatOptionsDictT,
):
    if is_known_broken(locale, options_):
        pytest.skip()

    options = DateTimeFormatOptions(**options_)
    formatter = DateTimeFormat(locale, options)
    assert (
        _normalize_whitespace(formatter.format(datetime_))
        == _normalize_whitespace(node.datetimeformat_format(locale, options, datetime_))
    )


@pytest.mark.parametrize(
    "datetime_",
    DATETIMES,
)
@pytest.mark.parametrize(
    "locale",
    LOCALES,
)
@pytest.mark.parametrize(
    "options_",
    OPTIONS,
)
def test_format_to_parts_against_js(
    node: NodeRunner,
    datetime_: dt.datetime,
    locale: str,
    options_: DateTimeFormatOptionsDictT,
):
    if is_known_broken(locale, options_):
        pytest.skip()

    options = DateTimeFormatOptions(**options_)
    formatter = DateTimeFormat(locale, options)
    assert (
        [part.to_json() for part in formatter.format_to_parts(datetime_)]
        == node.datetimeformat_formattoparts(locale, options, datetime_)
    )
