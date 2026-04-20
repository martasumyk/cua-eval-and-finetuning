import json
from datetime import datetime
from pathlib import Path


class JsonlLogger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, payload: dict):
        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **payload,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
