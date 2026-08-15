from __future__ import annotations

import re
import datetime as dt
from typing import TYPE_CHECKING

import pytest

from python_intl import DateTimeFormat

if TYPE_CHECKING:
    from python_intl.datetimeformat import DateTimeFormatOptionsDictT

    from .conftest import NodeRunner


WHITESPACE_RE = re.compile(r"\s")


def _normalize_whitespace(value: str) -> str:
    # Ensure we don't have any special whitespace like NBSP
    return WHITESPACE_RE.sub(" ", value)


@pytest.mark.parametrize(
    "locale",
    [
        "en-US",
        "en-GB",
        "de-DE",
        "de-AT",
        "sv-SE",
        "fr-FR",
        "it-IT",
    ],
)
@pytest.mark.parametrize(
    "options",
    [
        {"year": "numeric", "month": "2-digit", "day": "2-digit"},
        {"year": "numeric", "month": "long"},
        {"month": "long", "day": "numeric"},
        {"hour": "2-digit", "minute": "2-digit", "second": "2-digit"},
        {
            "year": "numeric",
            "month": "2-digit",
            "day": "2-digit",
            "hour": "2-digit",
            "minute": "2-digit",
            "second": "2-digit",
            "era": "long",
            "time_zone_name": "long",
            "weekday": "long",
            "fraction_second_digits": 3,
        },
    ],
)
def test_full_numeric_date(node: NodeRunner, locale: str, options: DateTimeFormatOptionsDictT):
    datetime_ = dt.datetime(2026, 8, 15)
    formatter = DateTimeFormat(locale, options)
    assert (
        _normalize_whitespace(formatter.format(datetime_))
        == _normalize_whitespace(node.datetimeformat(locale, options, datetime_))
    )
