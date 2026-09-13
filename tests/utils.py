import re

WHITESPACE_RE = re.compile(r"\s")
DATETIME_RANGE_WHITESPACE_RE = re.compile("\\s?\u2013\\s?")
NUMBER_RANGE_WHITESPACE_RE = re.compile("\\s?[\u2012\u2013-]\\s?")


def normalize_whitespace(value: str) -> str:
    # Ensure we don't have any special whitespace like NBSP
    return WHITESPACE_RE.sub(" ", value)


def normalize_datetime_range_whitespace(
    value: str,
    *,
    for_node: bool = False,
) -> str:
    # Ensure we don't have any special whitespace like NBSP
    return WHITESPACE_RE.sub(
        " ",
        DATETIME_RANGE_WHITESPACE_RE.sub(
            " - " if for_node else " \u2013 ",
            value,
        ),
    )


def normalize_number_range_whitespace(
    value: str,
    *,
    for_node: bool = False,
) -> str:
    # Ensure we don't have any special whitespace like NBSP
    return WHITESPACE_RE.sub(
        " ",
        NUMBER_RANGE_WHITESPACE_RE.sub(
            " - " if for_node else " \u2013 ",
            value,
        ),
    )


def normalize_parts_whitespace(
    parts: list[dict[str, str]],
    *,
    for_node: bool = False,
    for_range: bool = False,
) -> list[dict[str, str]]:
    def _normalize_part_value(part: dict[str, str]) -> dict[str, str]:
        if "value" not in part:
            return part

        return {
            **part,
            "value": (
                normalize_datetime_range_whitespace(part["value"], for_node=for_node)
                if for_range
                else normalize_whitespace(part["value"])
            ),
        }

    return [
        _normalize_part_value(part)
        for part
        in parts
    ]
