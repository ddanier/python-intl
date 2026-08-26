from __future__ import annotations

from functools import cached_property

import icu  # type: ignore[import-untyped]


class Locale:
    tag: str

    def __init__(self, tag: str) -> None:
        self.tag = tag

    @cached_property
    def _icu_locale(self) -> icu.Locale:  # ty: ignore[unresolved-attribute]
        return icu.Locale(self.tag)  # ty: ignore[unresolved-attribute]
