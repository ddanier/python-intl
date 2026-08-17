import datetime as dt

import python_intl as Intl
from python_intl.datetimeformat import DateTimeFormatOptions, _options_to_possible_skeletons


def print_formats(name: str, options: DateTimeFormatOptions) -> None:
    now = dt.datetime.now()
    print(name)  # noqa: T201
    print("Selected options")  # noqa: T201
    print(options.to_json())  # noqa: T201
    print(f"Possible skeleton codes: {', '.join(list(_options_to_possible_skeletons(options)))}")  # noqa: T201
    print("Format string and formatted date per locale")  # noqa: T201
    for locale_str in ("en", "en-GB", "sv", "de", "it", "fr", "no"):
        formatter = Intl.DateTimeFormat(locale=locale_str, options=options)
        format_pattern = formatter.matched_pattern
        formatted_datetime = formatter.format(now)
        print(f"- {locale_str}: {format_pattern} => {formatted_datetime}")  # noqa: T201
    print()  # noqa: T201


def main() -> None:
    print_formats(
        "FULL DATE",
        DateTimeFormatOptions(
            year="numeric",
            month="2-digit",
            day="2-digit",
        ),
    )
    print_formats(
        "MONTH & YEAR",
        DateTimeFormatOptions(
            month="long",
            year="numeric",
        ),
    )
    print_formats(
        "DAY IN MONTH",
        DateTimeFormatOptions(
            month="long",
            day="numeric",
        ),
    )
    print_formats(
        "DAY IN MONTH WITH WEEKDAY",
        DateTimeFormatOptions(
            month="long",
            day="numeric",
            weekday="long",
        ),
    )
    print_formats(
        "SHORT DAY IN MONTH WITH WEEKDAY",
        DateTimeFormatOptions(
            month="short",
            day="numeric",
            weekday="short",
        ),
    )
    print_formats(
        "TIME",
        DateTimeFormatOptions(
            hour="2-digit",
            minute="2-digit",
            second="2-digit",
        ),
    )
    print_formats(
        "EVERYTHING ALL AT ONCE",
        DateTimeFormatOptions(
            year="numeric",
            month="long",
            day="numeric",
            weekday="long",
            hour="2-digit",
            minute="2-digit",
            second="2-digit",
            time_zone_name="long",
        ),
    )


if __name__ == "__main__":
    main()
