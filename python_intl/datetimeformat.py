from __future__ import annotations

import dataclasses
import datetime as dt
from functools import cache, cached_property
from typing import TYPE_CHECKING, Literal, overload

import icu  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import NotRequired, TypedDict


if TYPE_CHECKING:
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

    type EraPatternT = Literal["G", "GGGG", "GGGGG"]
    type YearPatternT = Literal["y", "yy", "yyyy"]
    type MonthPatternT = Literal["M", "MM", "MMM", "MMMM", "MMMMM"]
    type WeekdayPatternT = Literal["E", "EEEE", "EEEEE"]
    type DayPatternT = Literal["d", "dd"]
    type DayPeriodPatternT = Literal["a", "aaaa", "aaaaa", "b", "bbbb", "bbbbb", "B", "BBBB", "BBBBB"]
    type HourPatternT = Literal["j", "jj", "H", "h", "HH", "hh"]
    type MinutePatternT = Literal["m", "mm"]
    type SecondPatternT = Literal["s", "ss"]
    type FractionSecondDigitsPatternT = Literal["S", "SS", "SSS"]
    type TimezoneNamePatternT = Literal["z", "zzzz", "Z", "ZZZZ", "v", "vvvv"]
    type AnyPatternT = (
        EraPatternT
        | YearPatternT
        | MonthPatternT
        | WeekdayPatternT
        | DayPatternT
        | DayPeriodPatternT
        | HourPatternT
        | MinutePatternT
        | SecondPatternT
        | FractionSecondDigitsPatternT
        | TimezoneNamePatternT
    )

    type DatetimeFieldT = Literal[
        "era",
        "year",
        "month",
        "weekday",
        "day",
        "day_period",
        "hour",
        "minute",
        "second",
        "fraction_second_digits",
        "time_zone_name",
    ]

    class DateTimeFormatOptionsDictT(TypedDict):
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

    class OptionsToSkeletonT(TypedDict):
        era: dict[EraFormatT, EraPatternT | tuple[EraPatternT, ...]]
        year: dict[YearFormatT, YearPatternT | tuple[YearPatternT, ...]]
        month: dict[MonthFormatT, MonthPatternT | tuple[MonthPatternT, ...]]
        weekday: dict[WeekdayFormatT, WeekdayPatternT | tuple[WeekdayPatternT, ...]]
        day: dict[DayFormatT, DayPatternT | tuple[DayPatternT, ...]]
        day_period: dict[DayPeriodFormatT, DayPeriodPatternT | tuple[DayPeriodPatternT, ...]]
        hour: dict[HourFormatT, HourPatternT | tuple[HourPatternT, ...]]
        minute: dict[MinuteFormatT, MinutePatternT | tuple[MinutePatternT, ...]]
        second: dict[SecondFormatT, SecondPatternT | tuple[SecondPatternT, ...]]
        fraction_second_digits: dict[
            FractionSecondDigitsFormatT,
            FractionSecondDigitsPatternT | tuple[FractionSecondDigitsPatternT, ...],
        ]
        time_zone_name: dict[TimezoneNameFormatT, TimezoneNamePatternT | tuple[TimezoneNamePatternT, ...]]


@dataclasses.dataclass(frozen=True, kw_only=True)
class DateTimeFormatOptions:
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
                ("day_period", self.day_period),
                ("hour", self.hour),
                ("minute", self.minute),
                ("second", self.second),
                ("fraction_second_digits", self.fraction_second_digits),
                ("time_zone_name", self.time_zone_name),
            )
            if v is not None
        }


OPTIONS_TO_SKELETON: OptionsToSkeletonT = {
    "era": {"short": "G", "long": "GGGG", "narrow": "GGGGG"},
    "year": {"numeric": ("yyyy", "y"), "2-digit": "yy"},
    "month": {"numeric": "M", "2-digit": "MM", "short": "MMM", "long": "MMMM", "narrow": "MMMMM"},
    "weekday": {"short": "E", "long": "EEEE", "narrow": "EEEEE"},
    "day": {"numeric": "d", "2-digit": "dd"},
    "day_period": {
        "short": ("a", "b", "B"),
        "long": ("aaaa", "bbbb", "BBBB"),
        "narrow": ("aaaaa", "bbbbb", "BBBBB"),
    },
    "hour": {"numeric": ("j", "H", "h"), "2-digit": ("jj", "HH", "hh")},
    "minute": {"numeric": "m", "2-digit": "mm"},
    "second": {"numeric": "s", "2-digit": "ss"},
    "fraction_second_digits": {1: "S", 2: "SS", 3: "SSS"},
    "time_zone_name": {
        "short": "z",
        "long": "zzzz",
        "short_offset": "Z",
        "long_offset": "ZZZZ",
        "short_generic": "v",
        "long_generic": "vvvv",
    },
}


@overload
def _option_to_skeleton_bit(
    field: Literal["era"],
    format: EraFormatT,
) -> EraPatternT | tuple[EraPatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["year"],
    format: YearFormatT,
) -> YearPatternT | tuple[YearPatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["month"],
    format: MonthFormatT,
) -> MonthPatternT | tuple[MonthPatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["weekday"],
    format: WeekdayFormatT,
) -> WeekdayPatternT | tuple[WeekdayPatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["day"],
    format: DayFormatT,
) -> DayPatternT | tuple[DayPatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["day_period"],
    format: DayPeriodFormatT,
) -> DayPeriodPatternT | tuple[DayPeriodPatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["hour"],
    format: HourFormatT,
) -> HourPatternT | tuple[HourPatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["minute"],
    format: MinuteFormatT,
) -> MinutePatternT | tuple[MinutePatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["second"],
    format: SecondFormatT,
) -> SecondPatternT | tuple[SecondPatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["fraction_second_digits"],
    format: FractionSecondDigitsFormatT,
) -> FractionSecondDigitsPatternT | tuple[FractionSecondDigitsPatternT, ...]: ...
@overload
def _option_to_skeleton_bit(
    field: Literal["time_zone_name"],
    format: TimezoneNameFormatT,
) -> TimezoneNamePatternT | tuple[TimezoneNamePatternT, ...]: ...
def _option_to_skeleton_bit(
    field,
    format,
):
    return OPTIONS_TO_SKELETON[field][format]


def _options_to_possible_skeletons(options: DateTimeFormatOptions) -> Iterable[str]:
    datetime_code_bits: list[str | tuple[str, ...]] = []

    # For order see babel.dates.PATTERN_CHAR_ORDER
    if options.era:
        datetime_code_bits.append(_option_to_skeleton_bit("era", options.era))
    if options.year:
        datetime_code_bits.append(_option_to_skeleton_bit("year", options.year))
    if options.month:
        datetime_code_bits.append(_option_to_skeleton_bit("month", options.month))
    if options.weekday:
        datetime_code_bits.append(_option_to_skeleton_bit("weekday", options.weekday))
    if options.day:
        datetime_code_bits.append(_option_to_skeleton_bit("day", options.day))
    if options.day_period:
        datetime_code_bits.append(_option_to_skeleton_bit("day_period", options.day_period))
    if options.hour:
        datetime_code_bits.append(_option_to_skeleton_bit("hour", options.hour))
    if options.minute:
        datetime_code_bits.append(_option_to_skeleton_bit("minute", options.minute))
    if options.second:
        datetime_code_bits.append(_option_to_skeleton_bit("second", options.second))
    if options.fraction_second_digits:
        datetime_code_bits.append(
            _option_to_skeleton_bit("fraction_second_digits", options.fraction_second_digits),
        )
    if options.time_zone_name:
        datetime_code_bits.append(_option_to_skeleton_bit("time_zone_name", options.time_zone_name))

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

    yield from generate_skeletons("", datetime_code_bits)


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
