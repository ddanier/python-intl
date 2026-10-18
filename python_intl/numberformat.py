from __future__ import annotations

import dataclasses
import decimal
from functools import cached_property
from typing import TYPE_CHECKING

import icu

from ._utils import _FormattedPartSpan
from .locale import Locale

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Literal, NotRequired, TypedDict

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
    type NumberFormattedPartTypeT = Literal[
        "literal", "unknown",
        "integer", "group", "decimal", "fraction", "compact",
        "exponent_separator", "exponent_minus_sign", "exponent_integer",
        "nan", "infinity",
        "plus_sign", "minus_sign", "percent_sign",
        "unit", "currency",
    ]

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
_FORMATTED_FIELD_TO_TYPE: dict[icu.UNumberFormatFields, NumberFormattedPartTypeT] = {
    icu.UNumberFormatFields.INTEGER: "integer",
    icu.UNumberFormatFields.GROUPING_SEPARATOR: "group",
    icu.UNumberFormatFields.DECIMAL_SEPARATOR: "decimal",
    icu.UNumberFormatFields.FRACTION: "fraction",
    icu.UNumberFormatFields.COMPACT: "compact",
    icu.UNumberFormatFields.EXPONENT_SYMBOL: "exponent_separator",
    icu.UNumberFormatFields.EXPONENT_SIGN: "exponent_minus_sign",
    icu.UNumberFormatFields.EXPONENT: "exponent_integer",
    # TODO(ddanier): How to do these?
    # https://github.com/ddanier/python-intl/issues/5
    # icu.UNumberFormatFields.HOW??: "nan",
    # icu.UNumberFormatFields.HOW??: "infinity",
    # icu.UNumberFormatFields.HOW??: "plus_sign",
    icu.UNumberFormatFields.SIGN: "minus_sign",
    icu.UNumberFormatFields.PERCENT: "unit",
    icu.UNumberFormatFields.MEASURE_UNIT: "unit",
    icu.UNumberFormatFields.CURRENCY: "currency",
}
_FORMATTED_FIELD_TO_TYPE_OVERRIDES_BY_STYLE: dict[
    StyleT,
    dict[icu.UNumberFormatFields, NumberFormattedPartTypeT],
] = {
    "percent": {
        icu.UNumberFormatFields.PERCENT: "percent_sign",
    },
}
_COMPONENT_TO_JSON_MAP = {
    "exponent_separator": "exponentSeparator",
    "exponent_minus_sign": "exponentMinusSign",
    "exponent_integer": "exponentInteger",
    "plus_sign": "plusSign",
    "minus_sign": "minusSign",
    "percent_sign": "percentSign",
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


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class NumberFormattedPart:
    type: NumberFormattedPartTypeT
    value: str

    def to_json(self) -> dict[str, str]:
        return {
            "type": _COMPONENT_TO_JSON_MAP.get(self.type, self.type),
            "value": self.value,
        }


def _options_to_skeleton(options: NumberFormatOptions) -> str:
    skeleton_parts: list[str] = []

    match options.style:
        case "decimal":
            skeleton_parts.append("decimal-auto")
            skeleton_parts.append(".###")
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
            skeleton_parts.append(".###")
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

    def format_to_parts(self, value: NumberT, /) -> Iterable[NumberFormattedPart]:
        match value:
            case int():
                formatted = self._icu_number_formatter.formatIntToValue(value)
            case float():
                formatted = self._icu_number_formatter.formatDoubleToValue(value)
            case decimal.Decimal():
                formatted = self._icu_number_formatter.formatDecimalToValue(str(value).encode("ascii"))

        # Break result string into parts
        result_string = str(formatted)

        last_end = 0
        parts = list(formatted)

        # Parts are not in subsequent order, the lost might be something like for "123,456" ("," is the group):
        # * "integer" from char 0 to 7
        # * "group" from char 3 to 4
        # ...this means we need to find the next most suitable group based on the current position in the
        # formatted string and the available parts.
        def _next_parts() -> tuple[icu.ConstrainedFieldPosition, icu.ConstrainedFieldPosition | None] | None:
            next_parts = sorted(
                (
                    part for part in parts
                    if (
                        # Parts that follow the last part...
                        part.getStart() >= last_end
                        # ...or parts we already had, but didn't end yet
                        or (part.getStart() < last_end and part.getLimit() > last_end)
                    )
                ),
                key=lambda part: (
                    # Always prefer parts starting at the current position
                    0 if part.getStart() == last_end else 1,
                    # Then prefer the ones starting next to the current position, shorter ones preferred
                    part.getStart(),
                    part.getLimit(),
                ),
            )
            if not next_parts:
                return None

            return (
                next_parts[0],
                next_parts[1] if len(next_parts) > 1 else None,
            )

        while (next_parts := _next_parts()):
            part, subsequent_part = next_parts

            span = _FormattedPartSpan(
                # start cannot move to a previous position
                start=max(part.getStart(), last_end),
                # end is either the normal end of the span or it might be the start of a susequent
                # part of both overlap
                end=(
                    min(part.getLimit(), subsequent_part.getStart())
                    if subsequent_part and subsequent_part.getStart() > last_end
                    else part.getLimit()
                ),
            )
            if span.start > last_end:
                yield NumberFormattedPart(
                    type="literal",
                    value=result_string[last_end:span.start],
                )

            if part.getCategory() == icu.UFieldCategory.NUMBER:
                type_= _FORMATTED_FIELD_TO_TYPE.get(part.getField(), "unknown")
                if (
                    self.options.style in _FORMATTED_FIELD_TO_TYPE_OVERRIDES_BY_STYLE
                    and part.getField() in _FORMATTED_FIELD_TO_TYPE_OVERRIDES_BY_STYLE[self.options.style]
                ):
                    type_ = _FORMATTED_FIELD_TO_TYPE_OVERRIDES_BY_STYLE[self.options.style][part.getField()]
                yield NumberFormattedPart(
                    type=type_,
                    value=result_string[span.start:span.end],
                )

            last_end = span.end

        # Ensure we didn't miss anything at the end
        if last_end < len(result_string):
            yield NumberFormattedPart(
                type="literal",
                value=result_string[last_end:],
            )

    @cached_property
    def _icu_number_range_formatter(self) -> icu.LocalizedNumberRangeFormatter:
        skeleton = _options_to_skeleton(self.options)
        return (
            icu.NumberRangeFormatter
            .withLocale(self.locale._icu_locale)
            .numberFormatterBoth(icu.NumberFormatter.forSkeleton(skeleton))
        )

    def format_range(self, start_value: NumberT, end_value: NumberT, /) -> str:
        match start_value, end_value:
            case int(), int():
                return self._icu_number_range_formatter.formatIntRange(start_value, end_value)
            case float(), float():
                return self._icu_number_range_formatter.formatDoubleRange(start_value, end_value)
            case decimal.Decimal(), decimal.Decimal():
                return self._icu_number_range_formatter.formatDoubleRange(
                    # For some reason formatDecimalRange fails, so we fall back to floats
                    float(start_value),
                    float(end_value),
                )
            case _:
                error = "Both parameters passed to format_range must have the same type"
                raise ValueError(error)
