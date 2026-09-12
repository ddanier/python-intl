from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    import datetime as dt

    from python_intl.collator import CollatorOptions
    from python_intl.datetimeformat import DateTimeFormatOptions


class NodeRunner:
    node_executable: Path

    def __init__(self) -> None:
        which_node = subprocess.run(["which", "node"], capture_output=True, check=True)  # noqa: S607
        self.node_executable = Path(which_node.stdout.decode().strip())

    def _run_node(self, eval_str: str) -> str:
        node_result = subprocess.run([self.node_executable, "-e", eval_str], capture_output=True, check=True)  # noqa: S603
        return node_result.stdout.decode().strip()

    def datetimeformat_format(
        self,
        locale: str,
        options: DateTimeFormatOptions,
        datetime_: dt.datetime,
    ) -> str:
        result = json.loads(
            self._run_node(f"""
                const formatter = new Intl.DateTimeFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
                const date = new Date(Date.UTC(
                    {datetime_.year}, {datetime_.month - 1}, {datetime_.day},
                    {datetime_.hour}, {datetime_.minute}, {datetime_.second},
                    {datetime_.microsecond},
                ));
                console.log(JSON.stringify(formatter.format(date)));
            """),
        )
        assert isinstance(result, str)
        return result

    def datetimeformat_formattoparts(
        self,
        locale: str,
        options: DateTimeFormatOptions,
        datetime_: dt.datetime,
    ) -> list[dict[str, str]]:
        result = json.loads(
            self._run_node(f"""
                const formatter = new Intl.DateTimeFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
                const date = new Date(Date.UTC(
                    {datetime_.year}, {datetime_.month - 1}, {datetime_.day},
                    {datetime_.hour}, {datetime_.minute}, {datetime_.second},
                    {datetime_.microsecond},
                ));
                console.log(JSON.stringify(formatter.formatToParts(date)));
            """),
        )
        assert isinstance(result, list)
        assert all(isinstance(i, dict) for i in result)
        return result

    def datetimeformat_formatrange(
        self,
        locale: str,
        options: DateTimeFormatOptions,
        start_datetime: dt.datetime,
        end_datetime: dt.datetime,
    ) -> str:
        result = json.loads(
            self._run_node(f"""
                const formatter = new Intl.DateTimeFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
                const startDate = new Date(Date.UTC(
                    {start_datetime.year}, {start_datetime.month - 1}, {start_datetime.day},
                    {start_datetime.hour}, {start_datetime.minute}, {start_datetime.second},
                    {start_datetime.microsecond},
                ));
                const endDate = new Date(Date.UTC(
                    {end_datetime.year}, {end_datetime.month - 1}, {end_datetime.day},
                    {end_datetime.hour}, {end_datetime.minute}, {end_datetime.second},
                    {end_datetime.microsecond},
                ));
                console.log(JSON.stringify(formatter.formatRange(startDate, endDate)));
            """),
        )
        assert isinstance(result, str)
        return result

    def datetimeformat_formatrangetoparts(
        self,
        locale: str,
        options: DateTimeFormatOptions,
        start_datetime: dt.datetime,
        end_datetime: dt.datetime,
    ) -> list[dict[str, str]]:
        result = json.loads(
            self._run_node(f"""
                const formatter = new Intl.DateTimeFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
                const startDate = new Date(Date.UTC(
                    {start_datetime.year}, {start_datetime.month - 1}, {start_datetime.day},
                    {start_datetime.hour}, {start_datetime.minute}, {start_datetime.second},
                    {start_datetime.microsecond},
                ));
                const endDate = new Date(Date.UTC(
                    {end_datetime.year}, {end_datetime.month - 1}, {end_datetime.day},
                    {end_datetime.hour}, {end_datetime.minute}, {end_datetime.second},
                    {end_datetime.microsecond},
                ));
                console.log(JSON.stringify(formatter.formatRangeToParts(startDate, endDate)));
            """),
        )
        assert isinstance(result, list)
        assert all(isinstance(i, dict) for i in result)
        return result

    def collator_compare(
        self,
        locale: str,
        options: CollatorOptions,
        string_a: str,
        string_b: str,
    ) -> int:
        result = json.loads(
            self._run_node(f"""
                const collator = new Intl.Collator({json.dumps(locale)}, {json.dumps(options.to_json())});
                console.log(JSON.stringify(collator.compare({json.dumps(string_a)}, {json.dumps(string_b)})));
            """),
        )
        assert isinstance(result, int)
        return result


@pytest.fixture
def node() -> NodeRunner:
    return NodeRunner()
