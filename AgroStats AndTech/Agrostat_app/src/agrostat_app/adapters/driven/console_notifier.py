"""Driven Adapter: Console and Structured Telemetry Notifier.

Implements NotificationPort.
Logs audit alerts and pipeline lifecycle events.
Normative: SWEBOK Chapter 2 / Observer Pattern.
"""

from datetime import datetime
import json
import logging
from typing import Any, Dict, Optional

from agrostat_app.ports.out_notification_port import NotificationPort


class ConsoleTelemetryAdapter(NotificationPort):
    """Adapter printing telemetry and structured alerts to standard output and logger."""

    def __init__(self, logger_name: str = "AgrostatDS") -> None:
        self._logger = logging.getLogger(logger_name)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def send_alert(
        self,
        level: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Emits structured notification to console."""
        tags = {
            "INFO": "[INFO]",
            "WARNING": "[WARN]",
            "CRITICAL": "[CRIT]",
            "SUCCESS": "[OK]",
        }
        tag = tags.get(level.upper(), "[*]")
        formatted = f"{tag} [{title}] {message}"

        if metadata:
            formatted += f" | Detalle: {json.dumps(metadata, ensure_ascii=False)}"

        lvl = level.upper()
        if lvl in ["CRITICAL", "ERROR"]:
            self._logger.error(formatted)
        elif lvl == "WARNING":
            self._logger.warning(formatted)
        else:
            self._logger.info(formatted)
