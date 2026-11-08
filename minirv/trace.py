"""Trace de execução: lista de registros (dicts) serializável em JSON."""
import json
from pathlib import Path


def hex32(value):
    return f"0x{value & 0xFFFFFFFF:08X}"


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
