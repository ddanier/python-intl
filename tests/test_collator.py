from __future__ import annotations

import datetime as dt
import re
from typing import TYPE_CHECKING

import pytest

from python_intl import Collator
from python_intl.collator import CollatorOptions

if TYPE_CHECKING:
    from python_intl.collator import CollatorOptionsDictT

    from .conftest import NodeRunner


# Note: We are not testing compare directly, as we can only test tiny bits of what you
#       normally intend to to. Instead all tests are using the sorted method instead, which
#       if a more realistic use case in general.


STRINGS_UMLAUTS = [
    "Adam",
    "Ädam",
    "ädam",
    "adam",
    "z",
]
STRINGS_NUMERIC = [
    "10 x",
    "1 x",
    "2 x",
    "2a",
]


@pytest.mark.parametrize(
    ("locale", "options_", "input_list", "expectation"),
    [
        ("en", {}, STRINGS_UMLAUTS, ['adam', 'Adam', 'ädam', 'Ädam', 'z']),
        ("en-GB", {}, STRINGS_UMLAUTS, ['adam', 'Adam', 'ädam', 'Ädam', 'z']),
        ("de", {}, STRINGS_UMLAUTS, ['adam', 'Adam', 'ädam', 'Ädam', 'z']),
        ("dv-SE", {}, STRINGS_UMLAUTS, ['adam', 'Adam', 'ädam', 'Ädam', 'z']),
        ("en", {"case_first": "upper"}, STRINGS_UMLAUTS, ['Adam', 'adam', 'Ädam', 'ädam', 'z']),
        ("en-GB", {"case_first": "upper"}, STRINGS_UMLAUTS, ['Adam', 'adam', 'Ädam', 'ädam', 'z']),
        ("de", {"case_first": "upper"}, STRINGS_UMLAUTS, ['Adam', 'adam', 'Ädam', 'ädam', 'z']),
        ("dv-SE", {"case_first": "upper"}, STRINGS_UMLAUTS, ['Adam', 'adam', 'Ädam', 'ädam', 'z']),
        ("en", {"sensitivity": "base"}, STRINGS_UMLAUTS, ['Adam', 'Ädam', 'ädam', 'adam', 'z']),
        ("en-GB", {"sensitivity": "base"}, STRINGS_UMLAUTS, ['Adam', 'Ädam', 'ädam', 'adam', 'z']),
        ("de", {"sensitivity": "base"}, STRINGS_UMLAUTS, ['Adam', 'Ädam', 'ädam', 'adam', 'z']),
        ("dv-SE", {"sensitivity": "base"}, STRINGS_UMLAUTS, ['Adam', 'Ädam', 'ädam', 'adam', 'z']),
        ("en", {"numeric": True}, STRINGS_NUMERIC, ['1 x', '2 x', '2a', '10 x']),
        ("en-GB", {"numeric": True}, STRINGS_NUMERIC, ['1 x', '2 x', '2a', '10 x']),
        ("de", {"numeric": True}, STRINGS_NUMERIC, ['1 x', '2 x', '2a', '10 x']),
        ("dv-SE", {"numeric": True}, STRINGS_NUMERIC, ['1 x', '2 x', '2a', '10 x']),
        ("en", {"ignore_punctuation": True}, STRINGS_NUMERIC, ['10 x', '1 x', '2a', '2 x']),
        ("en-GB", {"ignore_punctuation": True}, STRINGS_NUMERIC, ['10 x', '1 x', '2a', '2 x']),
        ("de", {"ignore_punctuation": True}, STRINGS_NUMERIC, ['10 x', '1 x', '2a', '2 x']),
        ("dv-SE", {"ignore_punctuation": True}, STRINGS_NUMERIC, ['10 x', '1 x', '2a', '2 x']),
        ("en", {"numeric": True, "ignore_punctuation": True}, STRINGS_NUMERIC, ['1 x', '2a', '2 x', '10 x']),
        ("en-GB", {"numeric": True, "ignore_punctuation": True}, STRINGS_NUMERIC, ['1 x', '2a', '2 x', '10 x']),
        ("de", {"numeric": True, "ignore_punctuation": True}, STRINGS_NUMERIC, ['1 x', '2a', '2 x', '10 x']),
        ("dv-SE", {"numeric": True, "ignore_punctuation": True}, STRINGS_NUMERIC, ['1 x', '2a', '2 x', '10 x']),
    ],
)
def test_sorted(
    locale: str,
    options_: CollatorOptionsDictT,
    input_list: list[str],
    expectation: int,
):
    options = CollatorOptions(**options_)
    collator = Collator(locale, options)
    assert collator.sorted(input_list) == expectation
