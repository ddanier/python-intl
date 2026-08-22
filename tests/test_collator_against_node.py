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


STRINGS_PAIRS = [
    ("Adam", "Ädam"),
    ("Adam", "ädam"),
    ("Ädam", "ädam"),
    ("äöü", "ÄÖÜ"),
    ("10 X", "1 X"),
    ("10 X", "2 X"),
    ("2 ZZ", "2Z"),
]
LOCALES = [
    "en",
    "en-GB",
    "de",
    "de-AT",
    "sv-SE",
]
OPTIONS = [
    {},
    {"numeric": True},
    {"ignore_punctuation": True},
    {"sensitivity": "base"},
]


@pytest.mark.parametrize(
    ("string_a", "string_b"),
    STRINGS_PAIRS,
)
@pytest.mark.parametrize(
    "locale",
    LOCALES,
)
@pytest.mark.parametrize(
    "options_",
    OPTIONS,
)
@pytest.mark.node
def test_compare_against_js(
    node: NodeRunner,
    string_a: str,
    string_b: str,
    locale: str,
    options_: CollatorOptionsDictT,
):
    options = CollatorOptions(**options_)
    collator = Collator(locale, options)
    assert (
        collator.compare(string_a, string_b)
        == node.collator_compare(locale, options, string_a, string_b)
    )
