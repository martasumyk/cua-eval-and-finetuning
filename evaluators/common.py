import base64
import json
import os
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image

SYSTEM_PROMPT = (
    "You are an automated evaluator for a GUI agent.\n"
    "You will receive:\n"
    "1. The task the agent was asked to complete.\n"
    "2. A screenshot of the desktop after the final step.\n\n"
    "You must decide if the task is fully completed.\n\n"
    "Rules:\n"
    "- completed = true ONLY if the screen clearly shows the final desired state.\n"
    "- If it is unclear or partially done, completed = false.\n"
    "- Answer in strict JSON: "
    '{"completed": <true_or_false>, "reason": "short explanation"}.\n'
    "Do NOT include anything else besides that single JSON object."
)


def load_session_data(session_dir: str) -> dict[str, Any]:
    session_path = Path(session_dir)
    log_path = session_path / "session_log.json"

    if not log_path.exists():
        raise FileNotFoundError(f"session_log.json not found in {session_dir}")

    with open(log_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    steps = data.get("steps", [])
    if not steps:
        raise ValueError("No steps found in session_log.json")

    last_step = steps[-1]
    task = data.get("task", "")
    screenshot_path = last_step.get("screenshot_path")

    if not screenshot_path:
        raise ValueError("No screenshot_path found for the last step")

    screenshot_path = (
        str((session_path / screenshot_path).resolve())
        if not Path(screenshot_path).is_absolute()
        else screenshot_path
    )

    return {
        "task": task,
        "last_step": last_step,
        "screenshot_path": screenshot_path,
        "session_path": str(session_path.resolve()),
    }


def load_image_rgb(image_path: str) -> Image.Image:
    return Image.open(image_path).convert("RGB")


def encode_image_to_base64(image_path: str, image_format: str = "PNG") -> str:
    image = load_image_rgb(image_path)
    buf = BytesIO()
    image.save(buf, format=image_format)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def encode_image_to_data_url(image_path: str, media_type: str = "image/png") -> str:
    return f"data:{media_type};base64,{encode_image_to_base64(image_path)}"


def build_user_prompt(task: str) -> str:
    return (
        f"Task:\n{task}\n\n"
        "Question:\nDoes the current screen show that the task is completed?\n"
        "Remember: respond in strict JSON."
    )


def extract_text_from_anthropic_content(content: list[Any]) -> str:
    parts: list[str] = []
    for block in content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
        elif isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(part for part in parts if part).strip()


def extract_json_object(text: str) -> dict[str, Any]:
    raw = text.strip()
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = raw[start:end + 1]
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    return {
        "completed": None,
        "reason": f"Could not parse as JSON. Raw output was: {raw}",
    }


def finalize_result(
    result: dict[str, Any],
    *,
    task: str,
    screenshot_path: str,
    evaluator_name: str,
    model_name: str,
) -> dict[str, Any]:
    result["task"] = task
    result["screenshot_path"] = screenshot_path
    result["evaluator"] = evaluator_name
    result["model"] = model_name
    result["evaluated_at"] = datetime.now(timezone.utc).isoformat()
    return result


def save_result(session_dir: str, file_name: str, result: dict[str, Any]) -> str:
    out_path = Path(session_dir) / file_name
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return str(out_path)


def getenv_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} not set in environment / .env")
    return value
