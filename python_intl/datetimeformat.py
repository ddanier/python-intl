from __future__ import annotations

import dataclasses
import datetime as dt
from functools import cache, cached_property
from typing import TYPE_CHECKING, Literal

import icu  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import NotRequired, TypedDict


if TYPE_CHECKING:
    type LocaleMatcherT = Literal["best fit", "lookup"]
    type Hour12T = bool | None
    type HourCycleT = Literal["h11", "h12", "h23", "h24"] | None

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
    type AnyFormatT = (
        EraFormatT
        | YearFormatT
        | MonthFormatT
        | WeekdayFormatT
        | DayFormatT
        | DayPeriodFormatT
        | HourFormatT
        | MinuteFormatT
        | SecondFormatT
        | FractionSecondDigitsFormatT
        | TimezoneNameFormatT
    )

    # Important: Must be the same as DateTimeFormatOptions
    # (nothing is required, as this will be used to construct a
    # DateTimeFormatOptions instance, so default values apply then)
    class DateTimeFormatOptionsDictT(TypedDict):
        locale_matcher: NotRequired[LocaleMatcherT]
        hour12: NotRequired[Hour12T]
        hour_cycle: NotRequired[HourCycleT]

        era: NotRequired[EraFormatT]
        year: NotRequired[YearFormatT]
        month: NotRequired[MonthFormatT]
        weekday: NotRequired[WeekdayFormatT]
        day: NotRequired[DayFormatT]
        day_period: NotRequired[DayPeriodFormatT]
        hour: NotRequired[HourFormatT]
        minute: NotRequired[MinuteFormatT]
        second: NotRequired[SecondFormatT]
        fraction_second_digits: NotRequired[FractionSecondDigitsFormatT]
        time_zone_name: NotRequired[TimezoneNameFormatT]


_TIMEZONE_NAME_JS_MAPPING: dict[str | None, str] = {
    "short_offset": "shortOffset",
    "long_offset": "longOffset",
    "short_generic": "shortGeneric",
    "long_generic": "longGeneric",
}


@dataclasses.dataclass(frozen=True, kw_only=True)
class DateTimeFormatOptions:
    locale_matcher: LocaleMatcherT = "best fit"
    hour12: Hour12T = None
    hour_cycle: HourCycleT = None

    era: EraFormatT | None = None
    year: YearFormatT | None = None
    month: MonthFormatT | None = None
    weekday: WeekdayFormatT | None = None
    day: DayFormatT | None = None
    day_period: DayPeriodFormatT | None = None
    hour: HourFormatT | None = None
    minute: MinuteFormatT | None = None
    second: SecondFormatT | None = None
    fraction_second_digits: FractionSecondDigitsFormatT | None = None
    time_zone_name: TimezoneNameFormatT | None = None

    def to_json(self) -> dict[str, str | int]:
        return {
            k: v
            for k, v in (
                ("era", self.era),
                ("year", self.year),
                ("month", self.month),
                ("weekday", self.weekday),
                ("day", self.day),
                ("dayPeriod", self.day_period),
                ("hour", self.hour),
                ("minute", self.minute),
                ("second", self.second),
                ("fractionalSecondDigits", self.fraction_second_digits),
                ("timeZoneName", _TIMEZONE_NAME_JS_MAPPING.get(self.time_zone_name, self.time_zone_name)),
            )
            if v is not None
        }


def _options_to_possible_skeletons(options: DateTimeFormatOptions) -> Iterable[str]:
    skeleton_parts: list[str | tuple[str, ...]] = []

    # Note: The parts should be ordered from big to small.

    match options.era:
        case "short":
            skeleton_parts.append("G")
        case "long":
            skeleton_parts.append("GGGG")
        case "narrow":
            skeleton_parts.append("GGGGG")

    match options.year:
        case "numeric":
            skeleton_parts.append(("yyyy", "y"))
        case "2-digit":
            skeleton_parts.append("yy")

    match options.month:
        case "numeric":
            skeleton_parts.append("M")
        case "2-digit":
            skeleton_parts.append("MM")
        case "short":
            skeleton_parts.append("MMM")
        case "long":
            skeleton_parts.append("MMMM")
        case "narrow":
            skeleton_parts.append("MMMMM")

    match options.weekday:
        case "short":
            skeleton_parts.append("E")
        case "long":
            skeleton_parts.append("EEEE")
        case "narrow":
            skeleton_parts.append("EEEEE")

    match options.day:
        case "numeric":
            skeleton_parts.append("d")
        case "2-digit":
            skeleton_parts.append("dd")

    match options.day_period:
        case "short":
            skeleton_parts.append("B")
        case "long":
            skeleton_parts.append("BBBB")
        case "narrow":
            skeleton_parts.append("BBBBB")

    match (options.hour_cycle, options.hour12, options.hour):
        case ("h11", _, "numeric"):
            skeleton_parts.append(("aK", "K"))
        case ("h11", _, "2-digit"):
            skeleton_parts.append(("aKK", "KK"))
        case ("h12", _, "numeric"):
            skeleton_parts.append(("ah", "h"))
        case ("h12", _, "2-digit"):
            skeleton_parts.append(("ahh", "hh"))
        case ("h23", _, "numeric"):
            skeleton_parts.append("H")
        case ("h23", _, "2-digit"):
            skeleton_parts.append("HH")
        case ("h24", _, "numeric"):
            skeleton_parts.append("k")
        case ("h24", _, "2-digit"):
            skeleton_parts.append("kk")
        case (_, True, "numeric"):
            skeleton_parts.append(("ah", "h"))
        case (_, True, "2-digit"):
            skeleton_parts.append(("ahh", "hh"))
        case (_, False, "numeric"):
            skeleton_parts.append("H")
        case (_, False, "2-digit"):
            skeleton_parts.append("HH")
        case (_, _, "numeric"):
            skeleton_parts.append("j")
        case (_, _, "2-digit"):
            skeleton_parts.append(("jj", "j"))

    match options.minute:
        case "numeric":
            skeleton_parts.append("m")
        case "2-digit":
            skeleton_parts.append("mm")

    match options.second:
        case "numeric":
            skeleton_parts.append("s")
        case "2-digit":
            skeleton_parts.append("ss")

    if options.fraction_second_digits:
        skeleton_parts.append("S" * options.fraction_second_digits)

    match options.time_zone_name:
        case "short":
            skeleton_parts.append("z")
        case "long":
            skeleton_parts.append("zzzz")
        case "short_offset":
            skeleton_parts.append("Z")
        case "long_offset":
            skeleton_parts.append("ZZZZ")
        case "short_generic":
            skeleton_parts.append("v")
        case "long_generic":
            skeleton_parts.append("vvvv")

    def generate_skeletons(prefix: str, remaining: list[str | tuple[str, ...]]) -> Iterable[str]:
        if not remaining:
            yield prefix
            return

        next_bit = remaining[0]
        if isinstance(next_bit, tuple):
            for next_bit_variant in next_bit:
                yield from generate_skeletons(prefix + next_bit_variant, remaining[1:])
        else:
            yield from generate_skeletons(prefix + next_bit, remaining[1:])

    yield from generate_skeletons("", skeleton_parts)


@dataclasses.dataclass(frozen=True, kw_only=True)
class MatchedFormatPattern:
    skeleton: str
    pattern: str

    def __str__(self) -> str:
        return self.pattern


class FormatPatternNotFoundException(Exception):
    pass


@cache
def _options_to_format_pattern(
    locale: icu.Locale,  # ty: ignore[unresolved-attribute]
    options: DateTimeFormatOptions,
) -> MatchedFormatPattern:
    possible_skeletons = list(_options_to_possible_skeletons(options))

    generator = icu.DateTimePatternGenerator.createInstance(locale)  # ty: ignore[unresolved-attribute]

    # Try a perfect match
    for skeleton in possible_skeletons:
        pattern = generator.getPatternForSkeleton(skeleton)
        if pattern:
            return MatchedFormatPattern(
                skeleton=skeleton,
                pattern=pattern,
            )

    # Try to find best match
    if options.locale_matcher == "best fit":
        for skeleton in possible_skeletons:
            pattern = generator.getBestPattern(skeleton)
            if pattern:
                return MatchedFormatPattern(
                    skeleton=skeleton,
                    pattern=pattern,
                )

    raise FormatPatternNotFoundException("Didn't find pattern for desired options")


class DateTimeFormat:
    locale: str
    options: DateTimeFormatOptions

    def __init__(
        self,
        locale: str,
        options: DateTimeFormatOptions | DateTimeFormatOptionsDictT,
    ) -> None:
        self.locale = locale
        if isinstance(options, DateTimeFormatOptions):
            self.options = options
        else:
            self.options = DateTimeFormatOptions(**options)

    @cached_property
    def icu_locale(self) -> icu.Locale:  # ty: ignore[unresolved-attribute]
        return icu.Locale(self.locale)  # ty: ignore[unresolved-attribute]

    @cached_property
    def matched_pattern(self) -> MatchedFormatPattern:
        return _options_to_format_pattern(self.icu_locale, self.options)

    @cached_property
    def icu_pattern(self) -> str:
        return self.matched_pattern.pattern

    @cached_property
    def icu_date_format(self) -> icu.SimpleDateFormat:  # ty: ignore[unresolved-attribute]
        return icu.SimpleDateFormat(self.icu_pattern, self.icu_locale)  # ty: ignore[unresolved-attribute]

    def format(self, datetime_: dt.datetime, /) -> str:
        return self.icu_date_format.format(datetime_)
