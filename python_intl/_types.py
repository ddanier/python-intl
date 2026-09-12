from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

    type LocaleMatcherT = Literal["best fit", "lookup"]
    type Hour12T = bool
    type HourCycleT = Literal["h11", "h12", "h23", "h24"]

    # datetime
    type EraFormatT = Literal["long", "short", "narrow"]
    type YearFormatT = Literal["numeric", "2-digit"]
    type MonthFormatT = Literal["numeric", "2-digit", "long", "short", "narrow"]
    type WeekdayFormatT = Literal["long", "short", "narrow"]
    type DayFormatT = Literal["numeric", "2-digit"]
    type DayPeriodFormatT = Literal["long", "short", "narrow"]
    type HourFormatT = Literal["numeric", "2-digit"]
    type MinuteFormatT = Literal["numeric", "2-digit"]
    type SecondFormatT = Literal["numeric", "2-digit"]
    type FractionSecondDigitsFormatT = Literal[1, 2, 3]
    type TimezoneNameFormatT = Literal[
        "short",
        "long",
        "short_offset",
        "long_offset",
        "short_generic",
        "long_generic",
    ]

    # number
    type StyleT = Literal["decimal", "currency", "percent", "unit"]
    type CurrencyT = str  # 3 char ISO code
    type CurrencyDisplayT = Literal["code", "symbol", "narrow_symbol", "name"]
    type CurrencySignT = Literal["standard", "accounting"]
    type UnitT = Literal[
        # see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/supportedValuesOf#supported_unit_identifiers
        # for Intl reference
        # see https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classicu_1_1MeasureUnit.html
        # for ICU reference
        "acre",
        "bit",
        "byte",
        "celsius",
        "centimeter",
        "day",
        "degree",
        "fahrenheit",
        "fluid-ounce",
        "foot",
        "gallon",
        "gigabit",
        "gigabyte",
        "gram",
        "hectare",
        "hour",
        "inch",
        "kilobit",
        "kilobyte",
        "kilogram",
        "kilometer",
        "liter",
        "megabit",
        "megabyte",
        "meter",
        "microsecond",
        "mile",
        "mile-scandinavian",
        "milliliter",
        "millimeter",
        "millisecond",
        "minute",
        "month",
        "nanosecond",
        "ounce",
        "percent",
        "petabyte",
        "pound",
        "second",
        "stone",
        "terabit",
        "terabyte",
        "week",
        "yard",
        "year",
    ]
    type UnitDisplayT = Literal["short", "narrow", "long"]

    # collator
    # type UsageT = Literal["sort", "search"]
    # type CollationT = Literal["emoji", "pinyin", "stroke"]
    type CaseFirstT = Literal["upper", "lower", "false"]
    type SensitivityT = Literal["base", "accent", "case", "variant"]

    type ComparisonResultT = Literal[-1, 0, 1]
