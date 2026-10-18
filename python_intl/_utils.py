from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import icu


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class _FormattedPartSpan:
    start: int
    end: int

    @classmethod
    def empty(cls) -> _FormattedPartSpan:
        return cls(start=0, end=0)

    @classmethod
    def from_constrained_fieldposition(cls, position: icu.ConstrainedFieldPosition) -> _FormattedPartSpan:
        return cls(start=position.getStart(), end=position.getLimit())

    def __contains__(self, inner: _FormattedPartSpan) -> bool:
        return inner.start >= self.start and inner.end <= self.end
