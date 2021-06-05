import sys
from pathlib import Path
from typing import Dict, List

from rpidiag.constants import EVENTS_MAPPING, OCCURRED_EVENTS
from rpidiag.templates import build_summary


def get_summary(summary: Dict[str, str], occurred_keys: List[int]) -> str:
    events = [EVENTS_MAPPING[key] for key in occurred_keys]
    return build_summary(summary) + _get_events(events)


def check_save_permissions(logfile: Path) -> None:
    try:
        with open(logfile, "a+"):
            pass
    except PermissionError:
        print(
            f"Not allowed to save the log file to: {logfile}."
            "\nChange the log path or use sudo."
        )
        sys.exit()


def save_log(output: str, logfile: Path) -> None:
    with open(logfile, "a+") as file:
        file.write(output + "\n")


def _get_events(events: List[str]) -> str:
    if events:
        return OCCURRED_EVENTS + ", ".join(events)
    return ""
