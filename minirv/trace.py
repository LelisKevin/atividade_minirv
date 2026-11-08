"""Trace de execução: lista de registros (dicts) serializável em JSON."""
import json
from pathlib import Path

from minirv.word32 import para_hex32 as hex32  # noqa: F401  (reexportado para os demais módulos)


class Trace:
    def __init__(self):
        self.records = []

    def add(self, record):
        self.records.append(record)

    def __len__(self):
        return len(self.records)

    def to_json(self, indent=2):
        return json.dumps(self.records, indent=indent, ensure_ascii=False)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_json() + "\n", encoding="utf-8")
