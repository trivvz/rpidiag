import sys
from typing import Dict, List

from rpidiag.config import LOGFILE
from rpidiag.constants import EVENTS_MAPPING, OCCURRED_EVENTS
from rpidiag.templates import OUTPUT_TEMPLATE, SUMMARY_TEMPLATE


class OutputHandler:
    @classmethod
    def get_summary(
        cls, summary: Dict[str, str], occurred_keys: List[int]
    ) -> str:
        events = [EVENTS_MAPPING[key] for key in occurred_keys]
        return SUMMARY_TEMPLATE.substitute(summary) + cls._get_events(events)

    @staticmethod
    def _get_events(events: List[str]) -> str:
        if events:
            return OCCURRED_EVENTS + ", ".join(events)
        return ""

    @staticmethod
    def get_output(output_dict: Dict[str, str]) -> str:
        return OUTPUT_TEMPLATE.substitute(output_dict)

    @staticmethod
    def save_log(output: str) -> None:
        try:
            with open(LOGFILE, "a+") as file:
                file.write(output + "\n")
        except PermissionError:
            print(
                f"Not allowed to save the log file to: {LOGFILE}."
                "\nChange log path or use sudo."
            )
            sys.exit()
