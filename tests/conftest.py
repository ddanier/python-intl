from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from python_intl.datetimeformat import DateTimeFormatOptionsDictT

class NodeRunner:
    node_executable: Path

    def __init__(self) -> None:
        which_node = subprocess.run(["which", "node"], capture_output=True)  # noqa: S607
        self.node_executable = Path(which_node.stdout.decode().strip())

    def _run_node(self, eval_str: str) -> str:
        node_result = subprocess.run([self.node_executable, "-e", eval_str], capture_output=True)  # noqa: S603
        return node_result.stdout.decode().strip()

    def datetimeformat(self, locale: str, options: DateTimeFormatOptionsDictT, datetime_: dt.datetime) -> str:
        JS_OPTIONS_MAP = {
            "time_zone_name": "timeZoneName",
            "fraction_second_digits": "fractionalSecondDigits",
        }
        js_options = {
            JS_OPTIONS_MAP.get(k, k): v
            for k, v
            in options.items()
        }
        return self._run_node(f"""
            const formatter = new Intl.DateTimeFormat({json.dumps(locale)}, {json.dumps(js_options)});
            const date = new Date(
                {datetime_.year}, {datetime_.month - 1}, {datetime_.day},
                {datetime_.hour}, {datetime_.minute}, {datetime_.second}, {datetime_.microsecond},
            );
            console.log(formatter.format(date));
        """)


@pytest.fixture
def node():
    return NodeRunner()
