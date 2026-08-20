from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from python_intl.datetimeformat import DateTimeFormatOptions


class NodeRunner:
    node_executable: Path

    def __init__(self) -> None:
        which_node = subprocess.run(["which", "node"], capture_output=True)  # noqa: S607
        self.node_executable = Path(which_node.stdout.decode().strip())

    def _run_node(self, eval_str: str) -> str:
        node_result = subprocess.run([self.node_executable, "-e", eval_str], capture_output=True)  # noqa: S603
        return node_result.stdout.decode().strip()

    def datetimeformat_format(
        self,
        locale: str,
        options: DateTimeFormatOptions,
        datetime_: dt.datetime,
    ) -> str:
        return self._run_node(f"""
            const formatter = new Intl.DateTimeFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
            const date = new Date(
                {datetime_.year}, {datetime_.month - 1}, {datetime_.day},
                {datetime_.hour}, {datetime_.minute}, {datetime_.second}, {datetime_.microsecond},
            );
            console.log(formatter.format(date));
        """)

    def datetimeformat_formattoparts(
        self,
        locale: str,
        options: DateTimeFormatOptions,
        datetime_: dt.datetime,
    ) -> list[dict[str, Any]]:
        return json.loads(
            self._run_node(f"""
                const formatter = new Intl.DateTimeFormat({json.dumps(locale)}, {json.dumps(options.to_json())});
                const date = new Date(
                    {datetime_.year}, {datetime_.month - 1}, {datetime_.day},
                    {datetime_.hour}, {datetime_.minute}, {datetime_.second}, {datetime_.microsecond},
                );
                console.log(JSON.stringify(formatter.formatToParts(date)));
            """),
        )


@pytest.fixture
def node():
    return NodeRunner()
