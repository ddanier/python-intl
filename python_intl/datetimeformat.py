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

    type PatternPartTypeT = Literal[
        "literal", "unknown",
        "era", "year", "month", "weekday", "day", "day_period",
        "hour", "minute", "second", "fraction_second_digits",
        "time_zone_name",
    ]

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

_PATTERN_SYMBOLS = "GyYuUrQqMLqQdDFgEecabBhHkKmsSAzZOvVxX"  # includes unused
_PATTERN_SYMBOL_TO_TYPE: dict[str, PatternPartTypeT] = {
    "G": "era",
    "y": "year",
    "Y": "year",
    "u": "year",
    "U": "year",
    "r": "year",
    "M": "month",
    "E": "weekday",
    "e": "weekday",
    "c": "weekday",
    "d": "day",
    "a": "day_period",
    "b": "day_period",
    "C": "day_period",
    "h": "hour",
    "H": "hour",
    "k": "hour",
    "K": "hour",
    "m": "minute",
    "s": "second",
    "S": "fraction_second_digits",
    "z": "time_zone_name",
    "Z": "time_zone_name",
    "O": "time_zone_name",
    "v": "time_zone_name",
    "V": "time_zone_name",
    "x": "time_zone_name",
    "X": "time_zone_name",
}
_PATTERN_FIELD_TO_TYPE: dict[icu.UDateTimePatternField, PatternPartTypeT] = {  # ty: ignore[unresolved-attribute]
    icu.DateFormat.ERA_FIELD: "era",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.YEAR_FIELD: "year",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.MONTH_FIELD: "month",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.DAY_OF_WEEK_FIELD: "weekday",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.DATE_FIELD: "day",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.AM_PM_FIELD: "day_period",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.HOUR0_FIELD: "hour",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.HOUR1_FIELD: "hour",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.HOUR_OF_DAY0_FIELD: "hour",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.HOUR_OF_DAY1_FIELD: "hour",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.MINUTE_FIELD: "minute",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.SECOND_FIELD: "second",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.MILLISECOND_FIELD: "fraction_second_digits",  # ty: ignore[unresolved-attribute]
    icu.DateFormat.TIMEZONE_FIELD: "time_zone_name",  # ty: ignore[unresolved-attribute]
}
_PATTERN_QUOTE = "'"

_COMPONENT_TO_JSON_MAP: dict[str, str] = {
    "day_period": "dayPeriod",
    "fraction_second_digits": "fractionalSecondDigits",
    "time_zone_name": "timeZoneName",
}
_TIMEZONE_NAME_TO_JSON_MAP: dict[str | None, str] = {
    "short_offset": "shortOffset",
    "long_offset": "longOffset",
    "short_generic": "shortGeneric",
    "long_generic": "longGeneric",
}


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
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
                ("timeZoneName", _TIMEZONE_NAME_TO_JSON_MAP.get(self.time_zone_name, self.time_zone_name)),
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


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class _MatchedFormatPattern:
    skeleton: str
    pattern: str

    def __str__(self) -> str:
        return self.pattern


class FormatPatternNotFoundException(Exception):
    pass


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class DateTimePatternPart:
    type: PatternPartTypeT
    value: str
    _pattern: str | None = None

    def to_json(self) -> dict[str, str]:
        return {
            "type": _COMPONENT_TO_JSON_MAP.get(self.type, self.type),
            "value": self.value,
            # note: _pattern is internal and not available in JavaScript
        }


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class DateTimeIntervalPatternPart:
    type: PatternPartTypeT
    value: str
    source: Literal["start_range", "end_range", "shared"]

    def to_json(self) -> dict[str, str]:
        return {
            "type": _COMPONENT_TO_JSON_MAP.get(self.type, self.type),
            "value": self.value,
            "source": {
                "start_range": "startRange",
                "end_range": "endRange",
            }.get(self.source, self.source),
        }


@cache
def _options_to_format_pattern(
    locale: icu.Locale,  # ty: ignore[unresolved-attribute]
    options: DateTimeFormatOptions,
) -> _MatchedFormatPattern:
    possible_skeletons = list(_options_to_possible_skeletons(options))

    generator = icu.DateTimePatternGenerator.createInstance(locale)  # ty: ignore[unresolved-attribute]

    # Try a perfect match
    for skeleton in possible_skeletons:
        pattern = generator.getPatternForSkeleton(skeleton)
        if pattern:
            return _MatchedFormatPattern(
                skeleton=skeleton,
                pattern=pattern,
            )

    # Try to find best match
    if options.locale_matcher == "best fit":
        for skeleton in possible_skeletons:
            pattern = generator.getBestPattern(skeleton)
            if pattern:
                return _MatchedFormatPattern(
                    skeleton=skeleton,
                    pattern=pattern,
                )

    raise FormatPatternNotFoundException("Didn't find pattern for desired options")


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class _PartSpan:
    start: int
    end: int

    @classmethod
    def empty(cls) -> _PartSpan:
        return cls(start=0, end=0)

    @classmethod
    def from_constrained_fieldposition(cls, position: icu.ConstrainedFieldPosition) -> _PartSpan:  # ty: ignore[unresolved-attribute]
        return cls(start=position.getStart(), end=position.getLimit())

    def __contains__(self, inner: _PartSpan) -> bool:
        return inner.start >= self.start and inner.end <= self.end


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
    def _icu_locale(self) -> icu.Locale:  # ty: ignore[unresolved-attribute]
        return icu.Locale(self.locale)  # ty: ignore[unresolved-attribute]

    @cached_property
    def _matched_pattern(self) -> _MatchedFormatPattern:
        return _options_to_format_pattern(self._icu_locale, self.options)

    @cached_property
    def _icu_pattern(self) -> str:
        return self._matched_pattern.pattern

    @cached_property
    def _icu_date_format(self) -> icu.SimpleDateFormat:  # ty: ignore[unresolved-attribute]
        return icu.SimpleDateFormat(self._icu_pattern, self._icu_locale)  # ty: ignore[unresolved-attribute]

    def format(self, datetime_: dt.datetime, /) -> str:
        return self._icu_date_format.format(datetime_)

    def format_to_parts(self, datetime_: dt.datetime, /) -> Iterable[DateTimePatternPart]:
        # Based on https://github.com/unicode-org/icu/blob/6fb634d81d10dd4667fb3fbcd1f19d9b9b926e62/icu4c/source/i18n/smpdtfmt.cpp#L1060
        pattern = self._icu_pattern
        in_quote = False
        prev_char = ""
        pattern_length = len(pattern)
        count = 0
        i = 0
        literal_chars: list[str] = []
        while i < pattern_length:
            char = pattern[i]

            if char != prev_char and count > 0:
                yield DateTimePatternPart(
                    type=_PATTERN_SYMBOL_TO_TYPE.get(prev_char, "unknown"),
                    value=icu.SimpleDateFormat(prev_char * count, self._icu_locale).format(datetime_),  # ty: ignore[unresolved-attribute]
                    _pattern=prev_char * count,
                )
                count = 0

            if char == _PATTERN_QUOTE:
                if (i + 1) < pattern_length and pattern[i + 1] == _PATTERN_QUOTE:
                    literal_chars.append(_PATTERN_QUOTE)
                    i += 1
                else:
                    in_quote = not in_quote
            elif not in_quote and char in _PATTERN_SYMBOLS:
                if literal_chars:
                    yield DateTimePatternPart(
                        type="literal",
                        value="".join(literal_chars),
                    )
                    literal_chars = []
                prev_char = char
                count += 1
            else:
                literal_chars.append(char)

            i += 1

        if count > 0:
            yield DateTimePatternPart(
                type=_PATTERN_SYMBOL_TO_TYPE.get(prev_char, "unknown"),
                value=icu.SimpleDateFormat(prev_char * count, self._icu_locale).format(datetime_),  # ty: ignore[unresolved-attribute]
                _pattern=prev_char * count,
            )
            assert not literal_chars  # noqa: S101
        elif literal_chars:
            yield DateTimePatternPart(
                type="literal",
                value="".join(literal_chars),
            )

    @cached_property
    def _icu_dateinterval_format(self) -> icu.DateIntervalFormat:  # ty: ignore[unresolved-attribute]
        possible_skeletons = list(_options_to_possible_skeletons(self.options))
        return icu.DateIntervalFormat.createInstance(possible_skeletons[0], self._icu_locale)  # ty: ignore[unresolved-attribute]

    def format_range(
        self,
        start_datetime: dt.datetime,
        end_datetime: dt.datetime,
    ) -> str:
        icu_date_interval = icu.DateInterval(start_datetime, end_datetime)  # ty: ignore[unresolved-attribute]
        return self._icu_dateinterval_format.format(icu_date_interval)

    def format_range_to_parts(
        self,
        start_datetime: dt.datetime,
        end_datetime: dt.datetime,
    ) -> Iterable[DateTimeIntervalPatternPart]:
        icu_date_interval = icu.DateInterval(start_datetime, end_datetime)  # ty: ignore[unresolved-attribute]
        formatted = self._icu_dateinterval_format.formatToValue(icu_date_interval)

        # Find spans of both datetimes (used to determine which parts have which source)
        span_start = _PartSpan.empty()
        span_end = _PartSpan.empty()
        for part in formatted:
            if part.getCategory() == icu.UFieldCategory.DATE_INTERVAL_SPAN:  # ty: ignore[unresolved-attribute]
                match part.getField():
                    case 0:
                        span_start = _PartSpan.from_constrained_fieldposition(part)
                    case 1:
                        span_end = _PartSpan.from_constrained_fieldposition(part)

        def source_of(span: _PartSpan) -> Literal["start_range", "end_range", "shared"]:
            if span in span_start:
                return "start_range"
            elif span in span_end:
                return "end_range"
            else:
                return "shared"

        # Break result string into parts
        result_string = str(formatted)
        last_end = 0
        for part in formatted:
            span = _PartSpan.from_constrained_fieldposition(part)
            if span.start > last_end:
                yield DateTimeIntervalPatternPart(
                    type="literal",
                    value=result_string[last_end:span.start],
                    source=source_of(_PartSpan(start=last_end, end=span.start)),
                )

            if part.getCategory() == icu.UFieldCategory.DATE:  # ty: ignore[unresolved-attribute]
                yield DateTimeIntervalPatternPart(
                    type=_PATTERN_FIELD_TO_TYPE.get(part.getField(), "unknown"),
                    value=result_string[span.start:span.end],
                    source=source_of(span),
                )

            last_end = span.end

        # Ensure we didn't miss anything at the end
        if last_end < len(result_string):
            yield DateTimeIntervalPatternPart(
                type="literal",
                value=result_string[last_end:],
                source=source_of(_PartSpan(start=last_end, end=len(result_string))),
            )
