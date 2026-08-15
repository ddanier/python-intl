import datetime as dt

import pytest

from python_intl import DateTimeFormat


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
