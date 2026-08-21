from __future__ import annotations

import dataclasses
from functools import cached_property
from typing import TYPE_CHECKING, Literal

import icu  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from typing import NotRequired, TypedDict


if TYPE_CHECKING:
    from ._types import LocaleMatcherT

    # type UsageT = Literal["sort", "search"]
    # type CollationT = Literal["emoji", "pinyin", "stroke"]
    type CaseFirstT = Literal["upper", "lower", "false"]
    type SensitivityT = Literal["base", "accent", "case", "variant"]

    type ComparisonResultT = Literal[-1, 0, 1]

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


_COLLATOR_RESULT_TO_RESULT: dict[icu.UCollationResult, ComparisonResultT] = {  # ty: ignore[unresolved-attribute]
    icu.UCollationResult.LESS: -1,  # ty: ignore[unresolved-attribute]
    icu.UCollationResult.EQUAL: 0,  # ty: ignore[unresolved-attribute]
    icu.UCollationResult.GREATER: 1,  # ty: ignore[unresolved-attribute]
}


class Collator:
    locale: str
    options: CollatorOptions

    def __init__(
        self,
        locale: str,
        options: CollatorOptions | CollatorOptionsDictT | None = None,
    ) -> None:
        self.locale = locale
        if options is None:
            self.options = CollatorOptions()
        elif isinstance(options, CollatorOptions):
            self.options = options
        else:
            self.options = CollatorOptions(**options)

    @cached_property
    def _icu_locale(self) -> icu.Locale:  # ty: ignore[unresolved-attribute]
        return icu.Locale(self.locale)  # ty: ignore[unresolved-attribute]

    @cached_property
    def _icu_collator(self) -> icu.Collator:  # ty: ignore[unresolved-attribute]
        collator = icu.Collator.createInstance(self._icu_locale)  # ty: ignore[unresolved-attribute]

        if self.options.numeric:
            collator.setAttribute(icu.UCollAttribute.NUMERIC_COLLATION, icu.UCollAttributeValue.ON)  # ty: ignore[unresolved-attribute]

        if (
            self.options.ignore_punctuation
            or (
                self.options.ignore_punctuation is None
                and self._icu_locale.getLanguage() == "th"
            )
        ):
            collator.setAttribute(icu.UCollAttribute.ALTERNATE_HANDLING, icu.UCollAttributeValue.SHIFTED)  # ty: ignore[unresolved-attribute]

        match self.options.case_first:
            case "upper":
                collator.setAttribute(icu.UCollAttribute.CASE_FIRST, icu.UCollAttributeValue.UPPER_FIRST)  # ty: ignore[unresolved-attribute]
            case "lower":
                collator.setAttribute(icu.UCollAttribute.CASE_FIRST, icu.UCollAttributeValue.LOWER_FIRST)  # ty: ignore[unresolved-attribute]

        collator.setAttribute(icu.UCollAttribute.NORMALIZATION_MODE, icu.UCollAttributeValue.ON)  # ty: ignore[unresolved-attribute]
        match self.options.sensitivity:
            case "base":
                collator.setAttribute(icu.UCollAttribute.STRENGTH, icu.UCollAttributeValue.PRIMARY)  # ty: ignore[unresolved-attribute]
            case "accent":
                collator.setAttribute(icu.UCollAttribute.STRENGTH, icu.UCollAttributeValue.SECONDARY)  # ty: ignore[unresolved-attribute]
            case "case":
                collator.setAttribute(icu.UCollAttribute.STRENGTH, icu.UCollAttributeValue.TERTIARY)  # ty: ignore[unresolved-attribute]
            case "variant":
                collator.setAttribute(icu.UCollAttribute.STRENGTH, icu.UCollAttributeValue.QUATERNARY)  # ty: ignore[unresolved-attribute]

        return collator

    def compare(self, string_a: str, string_b: str) -> ComparisonResultT:
        return _COLLATOR_RESULT_TO_RESULT[self._icu_collator.compare(string_a, string_b)]
