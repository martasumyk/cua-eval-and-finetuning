from pathlib import Path

from research.common.openclaw_client import OpenClawClient
from research.common.image_utils import image_to_base64
from research.common.action_parser import extract_json, validate_action
from research.common.logger import JsonlLogger


SYSTEM_PROMPT = """
You are a desktop computer-use agent.
Return exactly one JSON action.

Allowed actions:
- {"action":"click","x":123,"y":456}
- {"action":"double_click","x":123,"y":456}
- {"action":"right_click","x":123,"y":456}
- {"action":"type","text":"..."}
- {"action":"hotkey","keys":["CTRL","L"]}
- {"action":"scroll","dx":0,"dy":-400}
- {"action":"drag","x1":100,"y1":100,"x2":300,"y2":300}
- {"action":"wait","seconds":1}
- {"action":"done","reason":"task completed"}
- {"action":"fail","reason":"cannot proceed"}

Return JSON only.
"""


class OpenClawOSWorldAgent:
    def __init__(self, result_dir="./research/results/openclaw_osworld"):
        self.client = OpenClawClient()
        self.history = []
        self.logger = JsonlLogger(Path(result_dir) / "trajectory.jsonl")

    def reset(self):
        self.history = []

    def predict(self, instruction: str, screenshot_path: str):
        screenshot_b64 = image_to_base64(screenshot_path)

        raw = self.client.infer(
            instruction=instruction,
            screenshot_b64=screenshot_b64,
            history=self.history,
            system_prompt=SYSTEM_PROMPT,
            extra={"benchmark": "osworld"},
        )

        action = validate_action(extract_json(raw))
        self.history.append(
            {
                "instruction": instruction,
                "screenshot_path": screenshot_path,
                "model_output": raw,
                "action": action,
            }
        )
        self.logger.log(self.history[-1])
        return action