from __future__ import annotations

import decimal
import json
import os
import subprocess
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    import datetime as dt
    from collections.abc import Generator

    from python_intl.collator import CollatorOptions
    from python_intl.datetimeformat import DateTimeFormatOptions
    from python_intl.numberformat import NumberFormatOptions, NumberT


class NodeRunner:
    node_executable: Path

    def __init__(self) -> None:
        which_node = subprocess.run(
            ["which", "node"],  # noqa: S607
            capture_output=True,
            check=True,
            text=True,
        )
        self.node_executable = Path(which_node.stdout.strip())

    @cached_property
    def _node(self) -> subprocess.Popen[str]:
        return subprocess.Popen(  # noqa: S603
            [
                self.node_executable,
                "-e",
                r"""
                    import { createInterface } from "node:readline"

                    let buffer = [];

                    for await (const line of createInterface({ input: process.stdin })) {
                        if (line == "__EXIT__") {
                            process.exit(0);
                        } else if (line == "__RUN__") {
                            try {
                                console.log(JSON.stringify(eval(buffer.join("\n"))));
                            } catch (e) {
                                console.log("__FAILED__");
                            } finally {
                                buffer = [];
                            }
                        } else {
                            buffer.push(line);
                        }
                    }
                """,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def exit(self) -> None:
        assert self._node.stdin
        self._node.stdin.write(os.linesep)
        self._node.stdin.write("__EXIT__")
        self._node.stdin.write(os.linesep)
        try:
            self._node.wait(1)
        except subprocess.TimeoutExpired:
            self._node.kill()

    def _run_node(self, eval_str: str) -> Any:  # noqa: ANN401
        assert self._node.stdin
        assert self._node.stdout
        self._node.stdin.write(eval_str)
        self._node.stdin.write(os.linesep)
        self._node.stdin.write("__RUN__")
        self._node.stdin.write(os.linesep)
        result = self._node.stdout.readline().rstrip(os.linesep)
        if result == "__FAILED__":
            rerun = subprocess.run(  # noqa: S603
                [self.node_executable, "-e", eval_str],
                capture_output=True,
                check=False,
                text=True,
            )
            error = f"Node execution failed with error:{os.linesep * 2}{rerun.stderr}"
            raise RuntimeError(error)
        return json.loads(result)

    def numberformat_format(
        self,
        locale: str,
        options: NumberFormatOptions,
        value: NumberT,
    ) -> str:
        result = self._run_node(f"""
            const formatter = new Intl.NumberFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
            const value = {str(value) if isinstance(value, decimal.Decimal) else json.dumps(value)};
            formatter.format(value);
        """)
        assert isinstance(result, str)
        return result

    def numberformat_formatrange(
        self,
        locale: str,
        options: NumberFormatOptions,
        start_value: NumberT,
        end_value: NumberT,
    ) -> str:
        start_value_repr = (
            str(start_value)
            if isinstance(start_value, decimal.Decimal)
            else json.dumps(start_value)
        )
        end_value_repr = (
            str(end_value)
            if isinstance(end_value, decimal.Decimal)
            else json.dumps(end_value)
        )
        result = self._run_node(f"""
            const formatter = new Intl.NumberFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
            const start_value = {start_value_repr};
            const end_value = {end_value_repr};
            formatter.formatRange(start_value, end_value);
        """)
        assert isinstance(result, str)
        return result

    def datetimeformat_format(
        self,
        locale: str,
        options: DateTimeFormatOptions,
        datetime_: dt.datetime,
    ) -> str:
        result = self._run_node(f"""
            const formatter = new Intl.DateTimeFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
            const date = new Date(Date.UTC(
                {datetime_.year}, {datetime_.month - 1}, {datetime_.day},
                {datetime_.hour}, {datetime_.minute}, {datetime_.second},
                {datetime_.microsecond},
            ));
            formatter.format(date);
        """)
        assert isinstance(result, str)
        return result

    def datetimeformat_formattoparts(
        self,
        locale: str,
        options: DateTimeFormatOptions,
        datetime_: dt.datetime,
    ) -> list[dict[str, str]]:
        result = self._run_node(f"""
            const formatter = new Intl.DateTimeFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
            const date = new Date(Date.UTC(
                {datetime_.year}, {datetime_.month - 1}, {datetime_.day},
                {datetime_.hour}, {datetime_.minute}, {datetime_.second},
                {datetime_.microsecond},
            ));
            formatter.formatToParts(date);
        """)
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
        result = self._run_node(f"""
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
            formatter.formatRange(startDate, endDate);
        """)
        assert isinstance(result, str)
        return result

    def datetimeformat_formatrangetoparts(
        self,
        locale: str,
        options: DateTimeFormatOptions,
        start_datetime: dt.datetime,
        end_datetime: dt.datetime,
    ) -> list[dict[str, str]]:
        result = self._run_node(f"""
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
            formatter.formatRangeToParts(startDate, endDate);
        """)
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
        result = self._run_node(f"""
            const collator = new Intl.Collator({json.dumps(locale)}, {json.dumps(options.to_json())});
            collator.compare({json.dumps(string_a)}, {json.dumps(string_b)});
        """)
        assert isinstance(result, int)
        return result


@pytest.fixture(scope="session")
def node() -> Generator[NodeRunner]:
    runner = NodeRunner()
    yield runner
    runner.exit()
