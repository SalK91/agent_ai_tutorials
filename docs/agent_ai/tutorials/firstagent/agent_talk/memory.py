from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import json


@dataclass
class JsonMemory:
    """A tiny JSON-file memory.

    Think of this as the simplest possible long-term store:
    - `read(key)`
    - `write(key, value)`

    File format: { "key": any_json_serializable_value, ... }
    """

    path: Path

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("{}", encoding="utf-8")

    def _load(self) -> Dict[str, Any]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError:
            return {}

    def _save(self, data: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def read(self, key: str, default: Any = None) -> Any:
        data = self._load()
        return data.get(key, default)

    def write(self, key: str, value: Any) -> None:
        data = self._load()
        data[key] = value
        self._save(data)

    def append_to_list(self, key: str, value: Any) -> None:
        data = self._load()
        current = data.get(key)
        if current is None:
            data[key] = [value]
        elif isinstance(current, list):
            current.append(value)
            data[key] = current
        else:
            data[key] = [current, value]
        self._save(data)
