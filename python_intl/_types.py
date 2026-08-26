from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

    type LocaleMatcherT = Literal["best fit", "lookup"]
    type Hour12T = bool
    type HourCycleT = Literal["h11", "h12", "h23", "h24"]

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

    # type UsageT = Literal["sort", "search"]
    # type CollationT = Literal["emoji", "pinyin", "stroke"]
    type CaseFirstT = Literal["upper", "lower", "false"]
    type SensitivityT = Literal["base", "accent", "case", "variant"]

    type ComparisonResultT = Literal[-1, 0, 1]
