from __future__ import annotations

from functools import cached_property
from typing import override

import icu


class Locale:
    tag: str

    def __init__(self, tag: str) -> None:
        self.tag = tag

    @cached_property
    def _icu_locale(self) -> icu.Locale:
        return icu.Locale(self.tag)

    @override
    def __repr__(self) -> str:
        return f"Locale(tag={self.tag!r})"
