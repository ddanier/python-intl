from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from python_intl import NumberFormat, NumberFormatOptions

from .utils import normalize_number_range_whitespace, normalize_whitespace

if TYPE_CHECKING:
    from python_intl.numberformat import NumberFormatOptionsDictT


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("de-DE", "1.234,567"),
        ("en-US", "1,234.567"),
        ("en-GB", "1,234.567"),
        ("fr-FR", "1 234,567"),
        # "it" breaks based on ICU version, cause the thousand separator might be missing
        # ("it-IT", "1234,567"),
        ("sv-SE", "1 234,567"),
    ],
)
@pytest.mark.unit
def test_decimal_format(locale: str, expected: str):
    options = NumberFormatOptions(style="decimal")
    formatter = NumberFormat(locale, options)
    assert normalize_whitespace(formatter.format(1234.567)) == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("de-DE", "123.457 %"),
        ("en-US", "123,457%"),
        ("en-GB", "123,457%"),
        ("fr-FR", "123 457 %"),
        ("it-IT", "123.457%"),
        ("sv-SE", "123 457 %"),
    ],
)
@pytest.mark.unit
def test_percent_format(locale: str, expected: str):
    options = NumberFormatOptions(style="percent")
    formatter = NumberFormat(locale, options)
    assert normalize_whitespace(formatter.format(1234.567)) == expected


@pytest.mark.parametrize(
    ("locale", "options_", "expected"),
    [
        ("de-DE", {"unit": "liter"}, "1.234,567 l"),
        ("en-US", {"unit": "liter"}, "1,234.567 L"),
        ("en-GB", {"unit": "liter"}, "1,234.567 l"),
        ("fr-FR", {"unit": "liter"}, "1 234,567 l"),
        # "it" breaks based on ICU version, cause the thousand separator might be missing
        # ("it-IT", {"unit": "liter"}, "1234,567 l"),
        ("sv-SE", {"unit": "liter"}, "1 234,567 l"),
        ("de-DE", {"unit": "liter", "unit_display": "long"}, "1.234,567 Liter"),
        ("en-US", {"unit": "liter", "unit_display": "long"}, "1,234.567 liters"),
        ("en-GB", {"unit": "liter", "unit_display": "long"}, "1,234.567 litres"),
        ("fr-FR", {"unit": "liter", "unit_display": "long"}, "1 234,567 litres"),
        # "it" breaks based on ICU version, cause the thousand separator might be missing
        # ("it-IT", {"unit": "liter", "unit_display": "long"}, "1234,567 litri"),
        ("sv-SE", {"unit": "liter", "unit_display": "long"}, "1 234,567 liter"),
    ],
)
@pytest.mark.unit
def test_unit_format(locale: str, options_: NumberFormatOptionsDictT, expected: str):
    full_options_dict: NumberFormatOptionsDictT = {
        **options_,
        "style": "unit",
    }
    options = NumberFormatOptions(**full_options_dict)
    formatter = NumberFormat(locale, options)
    assert normalize_whitespace(formatter.format(1234.567)) == expected


@pytest.mark.parametrize(
    ("locale", "options_", "expected"),
    [
        ("de-DE", {"currency": "EUR"}, "1.234,57 €"),
        ("en-US", {"currency": "EUR"}, "€1,234.57"),
        ("en-GB", {"currency": "EUR"}, "€1,234.57"),
        ("fr-FR", {"currency": "EUR"}, "1 234,57 €"),
        # "it" breaks based on ICU version, cause the thousand separator might be missing
        # ("it-IT", {"currency": "EUR"}, "1234,57 €"),
        ("sv-SE", {"currency": "EUR"}, "1 234,57 €"),
        ("de-DE", {"currency": "EUR", "currency_display": "name"}, "1.234,57 Euro"),
        ("en-US", {"currency": "EUR", "currency_display": "name"}, "1,234.57 euros"),
        ("en-GB", {"currency": "EUR", "currency_display": "name"}, "1,234.57 euros"),
        ("fr-FR", {"currency": "EUR", "currency_display": "name"}, "1 234,57 euros"),
        # "it" breaks based on ICU version, cause the thousand separator might be missing
        # ("it-IT", {"currency": "EUR", "currency_display": "name"}, "1234,57 euro"),
        ("sv-SE", {"currency": "EUR", "currency_display": "name"}, "1 234,57 euro"),
    ],
)
@pytest.mark.unit
def test_currency_format(locale: str, options_: NumberFormatOptionsDictT, expected: str):
    full_options_dict: NumberFormatOptionsDictT = {
        **options_,
        "style": "currency",
    }
    options = NumberFormatOptions(**full_options_dict)
    formatter = NumberFormat(locale, options)
    assert normalize_whitespace(formatter.format(1234.567)) == expected


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("de-DE", "1.234,567\u20139.876,54321 l"),
        ("en-US", "1,234.567\u20139,876.54321 L"),
        ("en-GB", "1,234.567\u20139,876.54321 l"),
        ("fr-FR", "1 234,567\u20139 876,54321 l"),
        # "it" breaks based on ICU version, cause the thousand separator might be missing
        # ("it-IT", "1234,567\u20139876,54321 l"),
        ("sv-SE", "1 234,567\u20139 876,54321 l"),
    ],
)
@pytest.mark.unit
def test_unit_format_range(locale: str, expected: str):
    options = NumberFormatOptions(style="unit", unit="liter")
    formatter = NumberFormat(locale, options)
    assert normalize_number_range_whitespace(formatter.format_range(1234.567, 9876.54321)) == expected
