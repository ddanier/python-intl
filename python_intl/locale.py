from __future__ import annotations

from functools import cached_property

import icu


class Locale:
    tag: str

    def __init__(self, tag: str) -> None:
        self.tag = tag

    @cached_property
    def _icu_locale(self) -> icu.Locale:
        return icu.Locale(self.tag)
