"""Driven Adapter: JSON Dead Letter Queue (DLQ).

Implements DeadLetterQueuePort.
Appends quarantined records with reasons to a persistent JSONL audit log.
Normative: DAMA-BOK / Hexagonal Driven Adapter.
"""

from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List

from agrostat_app.ports.out_dlq_port import DeadLetterQueuePort


class JsonDeadLetterQueueAdapter(DeadLetterQueuePort):
    """Adapter storing quarantined error records in a JSONL file."""

    def __init__(self, dlq_dir: Path) -> None:
        self._dlq_dir = Path(dlq_dir)
        self._dlq_dir.mkdir(parents=True, exist_ok=True)
        self._dlq_file = self._dlq_dir / "quarantine_records.jsonl"

    def send_to_quarantine(self, quarantined_records: List[Dict[str, Any]]) -> int:
        """Appends quarantined error records to the DLQ file."""
        if not quarantined_records:
            return 0

        with open(self._dlq_file, "a", encoding="utf-8") as f:
            for item in quarantined_records:
                payload = {
                    "quarantined_at": datetime.utcnow().isoformat(),
                    "payload": item,
                }
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")

        return len(quarantined_records)

    def get_quarantined_records(self) -> List[Dict[str, Any]]:
        """Reads all quarantined records from the DLQ file."""
        if not self._dlq_file.exists():
            return []

        results = []
        with open(self._dlq_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    results.append(json.loads(line.strip()))

        return results
