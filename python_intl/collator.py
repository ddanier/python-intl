from __future__ import annotations

import dataclasses
import functools
from functools import cached_property
from typing import TYPE_CHECKING, overload

import icu

from .locale import Locale

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import NotRequired, TypedDict

    from ._types import CaseFirstT, ComparisonResultT, LocaleMatcherT, SensitivityT

    # Important: Must be the same as CollatorOptions
    # (nothing is required, as this will be used to construct a
    # CollatorOptions instance, so default values apply then)
    class CollatorOptionsDictT(TypedDict):
        locale_matcher: NotRequired[LocaleMatcherT]
        # usage: NotRequired[UsageT | None]
        # collation: NotRequired[CollationT | None]
        numeric: NotRequired[bool]
        case_first: NotRequired[CaseFirstT]
        sensitivity: NotRequired[SensitivityT]
        ignore_punctuation: NotRequired[bool | None]


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class CollatorOptions:
    locale_matcher: LocaleMatcherT = "best fit"
    # usage: UsageT | None = None
    # collation: CollationT | None = None
    numeric: bool = False
    case_first: CaseFirstT = "false"
    sensitivity: SensitivityT = "variant"
    ignore_punctuation: bool | None = None

    def to_json(self) -> dict[str, str | int]:
        return {
            k: v
            for k, v in (
                ("localeMatcher", self.locale_matcher),
                # ("usage", self.usage),
                # ("collation", self.collation),
                ("numeric", self.numeric),
                ("caseFirst", self.case_first),
                ("sensitivity", self.sensitivity),
                ("ignorePunctuation", self.ignore_punctuation),
            )
            if v is not None
        }


_COLLATOR_RESULT_TO_RESULT: dict[icu.UCollationResult, ComparisonResultT] = {
    icu.UCollationResult.LESS: -1,
    icu.UCollationResult.EQUAL: 0,
    icu.UCollationResult.GREATER: 1,
}


class Collator:
    locale: Locale
    options: CollatorOptions

    def __init__(
        self,
        locale: Locale | str,
        options: CollatorOptions | CollatorOptionsDictT | None = None,
    ) -> None:
        if isinstance(locale, Locale):
            self.locale = locale
        else:
            self.locale = Locale(locale)
        if options is None:
            self.options = CollatorOptions()
        elif isinstance(options, CollatorOptions):
            self.options = options
        else:
            self.options = CollatorOptions(**options)

    @cached_property
    def _icu_collator(self) -> icu.Collator:
        collator = icu.Collator.createInstance(self.locale._icu_locale)

        if self.options.numeric:
            collator.setAttribute(icu.UCollAttribute.NUMERIC_COLLATION, icu.UCollAttributeValue.ON)

        if (
            self.options.ignore_punctuation
            or (
                self.options.ignore_punctuation is None
                and self.locale._icu_locale.getLanguage() == "th"
            )
        ):
            collator.setAttribute(icu.UCollAttribute.ALTERNATE_HANDLING, icu.UCollAttributeValue.SHIFTED)

        match self.options.case_first:
            case "upper":
                collator.setAttribute(icu.UCollAttribute.CASE_FIRST, icu.UCollAttributeValue.UPPER_FIRST)
            case "lower":
                collator.setAttribute(icu.UCollAttribute.CASE_FIRST, icu.UCollAttributeValue.LOWER_FIRST)

        collator.setAttribute(icu.UCollAttribute.NORMALIZATION_MODE, icu.UCollAttributeValue.ON)
        match self.options.sensitivity:
            case "base":
                collator.setAttribute(icu.UCollAttribute.STRENGTH, icu.UCollAttributeValue.PRIMARY)
            case "accent":
                collator.setAttribute(icu.UCollAttribute.STRENGTH, icu.UCollAttributeValue.SECONDARY)
            case "case":
                collator.setAttribute(icu.UCollAttribute.STRENGTH, icu.UCollAttributeValue.TERTIARY)
            case "variant":
                collator.setAttribute(icu.UCollAttribute.STRENGTH, icu.UCollAttributeValue.QUATERNARY)

        return collator

    def compare(self, string_a: str, string_b: str) -> ComparisonResultT:
        return _COLLATOR_RESULT_TO_RESULT[self._icu_collator.compare(string_a, string_b)]

    @overload
    def sorted(self, items: Iterable[str], /, key: None = None) -> Iterable[str]: ...
    @overload
    def sorted[T](self, items: Iterable[T], /, key: Callable[[T], str]) -> Iterable[T]: ...
    def sorted(self, items, /, key = None):  # pyright: ignore[reportInconsistentOverload]
        return sorted(
            items,
            key=functools.cmp_to_key(
                (lambda a, b: self.compare(key(a), key(b)))
                if key
                else self.compare,
            ),
        )
