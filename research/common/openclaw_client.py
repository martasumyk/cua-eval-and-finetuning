import time
import requests
from research.config import (
    OPENCLAW_BASE_URL,
    OPENCLAW_API_KEY,
    OPENCLAW_MODEL,
    OPENCLAW_TIMEOUT,
    OPENCLAW_MAX_RETRIES,
)


class OpenClawClient:
    def __init__(self):
        self.base_url = OPENCLAW_BASE_URL
        self.api_key = OPENCLAW_API_KEY
        self.model = OPENCLAW_MODEL
        self.timeout = OPENCLAW_TIMEOUT
        self.max_retries = OPENCLAW_MAX_RETRIES

    def infer(self, instruction, screenshot_b64, history=None, system_prompt="", extra=None):
        payload = {
            "instruction": instruction,
            "screenshot_b64": screenshot_b64,
            "history": history or [],
            "system_prompt": system_prompt,
            "model": self.model,
            "extra": extra or {},
        }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        last_err = None
        for attempt in range(self.max_retries):
            try:
                resp = requests.post(
                    f"{self.base_url}/infer",
                    json=payload,
                    headers=headers,
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                data = resp.json()
                return data["text"]
            except Exception as e:
                last_err = e
                if attempt + 1 < self.max_retries:
                    time.sleep(2 ** attempt)

        raise RuntimeError(f"OpenClaw inference failed: {last_err}")