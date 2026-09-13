from __future__ import annotations

import decimal
from typing import TYPE_CHECKING

import pytest

from python_intl import NumberFormat, NumberFormatOptions

from .utils import normalize_number_range_whitespace, normalize_whitespace

if TYPE_CHECKING:
    from python_intl._types import CurrencyT, UnitT
    from python_intl.numberformat import NumberFormatOptionsDictT, NumberT

    from .conftest import NodeRunner


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
VALUES: list[NumberT] = [
    123,
    123456,
    123.456,
    123.0,
    123.1,
    decimal.Decimal("123.456"),
]
RANGES: list[tuple[NumberT, NumberT]] = [
    (123, 456),
    (123456, 456789000),
    (123.0, 456.789),
    (decimal.Decimal("123.456"), decimal.Decimal("987.654")),
]
UNITS = [
    "celsius",
    "liter",
    "megabyte",
    "meter",
    "percent",
]
UNIT_OPTIONS = [
    {"unit_display": "short"},
    {"unit_display": "narrow"},
    {"unit_display": "long"},
]
CURRENCIES = [
    "EUR",
    "USD",
    "GBP",
    "SEK",
]
CURRENCY_OPTIONS = [
    {"currency_display": "code"},
    {"currency_display": "symbol"},
    {"currency_display": "narrow_symbol"},
    {"currency_display": "name"},
    {"currency_sign": "accounting"},
]


def is_known_broken(
    locale: str,
    options_: NumberFormatOptionsDictT,
) -> bool:
    # Sadly some formats don't match, skip for now
    return bool(
        # Differs between °C and only ° between ICU version
        (options_.get("unit") == "celsius")
        # "it" might not have thousand separator based on ICU version
        or (options_.get("style") in ("decimal", "currency", "unit") and locale == "it-IT"),
    )


@pytest.mark.parametrize(
    "locale",
    LOCALES,
)
@pytest.mark.parametrize(
    "value",
    VALUES,
)
def test_decimal_format(
    node: NodeRunner,
    locale: str,
    value: NumberT,
):
    options = NumberFormatOptions(style="decimal")
    formatter = NumberFormat(locale, options)
    assert (
        normalize_whitespace(formatter.format(value))
        == normalize_whitespace(node.numberformat_format(locale, options, value))
    )


@pytest.mark.parametrize(
    "locale",
    LOCALES,
)
@pytest.mark.parametrize(
    "value",
    VALUES,
)
def test_percent_format(
    node: NodeRunner,
    locale: str,
    value: NumberT,
):
    options = NumberFormatOptions(style="percent")
    formatter = NumberFormat(locale, options)
    assert (
        normalize_whitespace(formatter.format(value))
        == normalize_whitespace(node.numberformat_format(locale, options, value))
    )


@pytest.mark.parametrize(
    "locale",
    LOCALES,
)
@pytest.mark.parametrize(
    "value",
    VALUES,
)
@pytest.mark.parametrize(
    "unit",
    UNITS,
)
@pytest.mark.parametrize(
    "unit_options",
    UNIT_OPTIONS,
)
def test_unit_format(
    node: NodeRunner,
    locale: str,
    value: NumberT,
    unit: UnitT,
    unit_options: NumberFormatOptionsDictT,
):
    full_options_dict: NumberFormatOptionsDictT = {
        **unit_options,
        "unit": unit,
        "style": "unit",
    }

    if is_known_broken(locale, full_options_dict):
        pytest.skip()

    options = NumberFormatOptions(**full_options_dict)
    formatter = NumberFormat(locale, options)
    assert (
        normalize_whitespace(formatter.format(value))
        == normalize_whitespace(node.numberformat_format(locale, options, value))
    )


@pytest.mark.parametrize(
    "locale",
    LOCALES,
)
@pytest.mark.parametrize(
    "range_",
    RANGES,
)
@pytest.mark.parametrize(
    "unit",
    UNITS,
)
@pytest.mark.parametrize(
    "unit_options",
    UNIT_OPTIONS,
)
def test_unit_format_range(
    node: NodeRunner,
    locale: str,
    range_: tuple[NumberT, NumberT],
    unit: UnitT,
    unit_options: NumberFormatOptionsDictT,
):
    full_options_dict: NumberFormatOptionsDictT = {
        **unit_options,
        "unit": unit,
        "style": "unit",
    }

    if is_known_broken(locale, full_options_dict):
        pytest.skip()

    options = NumberFormatOptions(**full_options_dict)
    formatter = NumberFormat(locale, options)
    assert (
        normalize_number_range_whitespace(formatter.format_range(*range_), for_node=True)
        == normalize_number_range_whitespace(
            node.numberformat_formatrange(locale, options, *range_),
            for_node=True,
        )
    )


@pytest.mark.parametrize(
    "locale",
    LOCALES,
)
@pytest.mark.parametrize(
    "value",
    VALUES,
)
@pytest.mark.parametrize(
    "currency",
    CURRENCIES,
)
@pytest.mark.parametrize(
    "currency_options",
    CURRENCY_OPTIONS,
)
def test_currency_format(
    node: NodeRunner,
    locale: str,
    value: NumberT,
    currency: CurrencyT,
    currency_options: NumberFormatOptionsDictT,
):
    full_options_dict: NumberFormatOptionsDictT = {
        **currency_options,
        "currency": currency,
        "style": "currency",
    }

    if is_known_broken(locale, full_options_dict):
        pytest.skip()

    options = NumberFormatOptions(**full_options_dict)
    formatter = NumberFormat(locale, options)
    assert (
        normalize_whitespace(formatter.format(value))
        == normalize_whitespace(node.numberformat_format(locale, options, value))
    )
