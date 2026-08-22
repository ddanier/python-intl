import re

WHITESPACE_RE = re.compile(r"\s")
RANGE_WHITESPACE_RE = re.compile(r"\s?–\s?")  # noqa: RUF001


def normalize_whitespace(value: str) -> str:
    # Ensure we don't have any special whitespace like NBSP
    return WHITESPACE_RE.sub(" ", value)


def normalize_range_whitespace(value: str) -> str:
    # Ensure we don't have any special whitespace like NBSP
    return WHITESPACE_RE.sub(" ", RANGE_WHITESPACE_RE.sub(" – ", value))  # noqa: RUF001


def normalize_parts_whitespace(parts: list[dict], *, for_range: bool = False) -> list[dict]:
    def _normalize_part_value(part: dict) -> dict:
        if "value" not in part:
            return part

        return {
            **part,
            "value": (
                normalize_range_whitespace(part["value"])
                if for_range
                else normalize_whitespace(part["value"])
            ),
        }

    return [
        _normalize_part_value(part)
        for part
        in parts
    ]
