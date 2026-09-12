from __future__ import annotations

import dataclasses
import decimal
from functools import cached_property
from typing import TYPE_CHECKING

import icu

from .locale import Locale

if TYPE_CHECKING:
    from typing import NotRequired, TypedDict

    from ._types import (
        CurrencyDisplayT,
        CurrencySignT,
        CurrencyT,
        LocaleMatcherT,
        StyleT,
        UnitDisplayT,
        UnitT,
    )

    type NumberT = decimal.Decimal | float | int

    # Important: Must be the same as DateTimeFormatOptions
    # (nothing is required, as this will be used to construct a
    # DateTimeFormatOptions instance, so default values apply then)
    class NumberFormatOptionsDictT(TypedDict):
        locale_matcher: NotRequired[LocaleMatcherT]

        style: NotRequired[StyleT]

        currency: NotRequired[CurrencyT]
        currency_display: NotRequired[CurrencyDisplayT]
        currency_sign: NotRequired[CurrencySignT]

        unit: NotRequired[UnitT]
        unit_display: NotRequired[UnitDisplayT]


_CURRENCY_DISPLAY_TO_JSON_MAP: dict[str, str] = {
    "narrow_symbol": "narrowSymbol",
}


class InvalidNumberFormatOptionError(ValueError):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class NumberFormatOptions:
    locale_matcher: LocaleMatcherT = "best fit"

    style: StyleT = "decimal"

    currency: CurrencyT | None = None
    currency_display: CurrencyDisplayT = "symbol"
    currency_sign: CurrencySignT = "standard"

    unit: UnitT | None = None
    unit_display: UnitDisplayT = "short"

    def __post_init__(self) -> None:
        error = None
        if self.style == "currency" and self.currency is None:
            error = "You need to provide a currency when using the currency style"
        elif self.style == "unit" and self.unit is None:
            error = "You need to provide a unit when using the unit style"

        if error:
            raise InvalidNumberFormatOptionError(error)

    def to_json(self) -> dict[str, str | int]:
        return {
            k: v
            for k, v in (
                ("localeMatcher", self.locale_matcher),

                ("style", self.style),

                ("currency", self.currency),
                ("currencyDisplay", _CURRENCY_DISPLAY_TO_JSON_MAP.get(
                    self.currency_display,
                    self.currency_display,
                )),
                ("currencySign", self.currency_sign),

                ("unit", self.unit),
                ("unitDisplay", self.unit_display),
            )
            if v is not None
        }


def _options_to_skeleton(options: NumberFormatOptions) -> str:
    skeleton_parts: list[str] = []

    match options.style:
        case "decimal":
            skeleton_parts.append("decimal-auto")
        case "percent":
            skeleton_parts.append("precision-integer")
            skeleton_parts.append("scale/100")
            skeleton_parts.append("percent")
        case "currency":
            skeleton_parts.append(f"currency/{options.currency}")
            skeleton_parts.append("precision-currency-standard")
            if options.currency_sign == "accounting":
                skeleton_parts.append("sign-accounting")
            match options.currency_display:
                case "code":
                    skeleton_parts.append("unit-width-iso-code")
                case "symbol":
                    skeleton_parts.append("unit-width-short")
                case "narrow_symbol":
                    skeleton_parts.append("unit-width-narrow")
                case "name":
                    skeleton_parts.append("unit-width-full-name")
        case "unit":
            skeleton_parts.append(f"unit/{options.unit}")
            match options.unit_display:
                case "short":
                    skeleton_parts.append("unit-width-short")
                case "narrow":
                    skeleton_parts.append("unit-width-narrow")
                case "long":
                    skeleton_parts.append("unit-width-full-name")

    return " ".join(skeleton_parts)


class NumberFormat:
    locale: Locale
    options: NumberFormatOptions

    def __init__(
        self,
        locale: Locale | str,
        options: NumberFormatOptions | NumberFormatOptionsDictT | None = None,
    ) -> None:
        if isinstance(locale, Locale):
            self.locale = locale
        else:
            self.locale = Locale(locale)
        if options is None:
            self.options = NumberFormatOptions()
        elif isinstance(options, NumberFormatOptions):
            self.options = options
        else:
            self.options = NumberFormatOptions(**options)

    @cached_property
    def _icu_number_formatter(self) -> icu.LocalizedNumberFormatter:
        skeleton = _options_to_skeleton(self.options)
        return icu.NumberFormatter.forSkeleton(skeleton).locale(self.locale._icu_locale)

    def format(self, value: NumberT, /) -> str:
        match value:
            case int():
                return self._icu_number_formatter.formatInt(value)
            case float():
                return self._icu_number_formatter.formatDouble(value)
            case decimal.Decimal():
                return self._icu_number_formatter.formatDecimal(str(value).encode("ascii"))
