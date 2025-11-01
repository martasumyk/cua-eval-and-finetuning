import os
import json
import base64
from typing import Dict, Any
from pathlib import Path
from PIL import Image
from io import BytesIO
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


def init_eval_client() -> OpenAI:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment / .env")

    return OpenAI(api_key=api_key)



def load_session_data(session_dir: str) -> Dict[str, Any]:
    session_path = Path(session_dir)
    log_path = session_path / "session_log.json"

    if not log_path.exists():
        raise FileNotFoundError(f"session_log.json not found in {session_dir}")

    with open(log_path, "r") as f:
        data = json.load(f)

    steps = data.get("steps", [])
    if not steps:
        raise ValueError("No steps found in session_log.json")

    last_step = steps[-1]
    task = data.get("task", "")
    screenshot_path = last_step.get("screenshot_path")

    return {
        "task": task,
        "last_step": last_step,
        "screenshot_path": screenshot_path,
    }



def encode_image_to_data_url(png_path: str) -> str:
    with Image.open(png_path) as img:
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return "data:image/png;base64," + b64


def build_eval_messages(task: str, screenshot_data_url: str) -> list[dict]:
    """
    We give GPT-4o:
    - system role: you're an evaluator
    - user content: (image + instructions)

    We'll ask it to output strict JSON so it's machine-parseable:
    { "completed": true/false, "reason": "..." }
    """
    system_prompt = (
        "You are an automated evaluator for a GUI agent.\n"
        "You will receive:\n"
        "1. The task the agent was asked to complete.\n"
        "2. A screenshot of the desktop after the final step.\n\n"
        "You must decide if the task is fully completed.\n\n"
        "Rules:\n"
        "- completed = true ONLY if the screen clearly shows the final desired state.\n"
        "- If it's unclear or partially done, completed = false.\n"
        "- Answer in strict JSON: "
        '{\"completed\": <true_or_false>, \"reason\": \"short explanation\"}.\n'
        "Do NOT include anything else besides that single JSON object."
    )

    user_instruction = (
        f"Task:\n{task}\n\n"
        "Question:\nDoes the current screen show that the task is completed?\n"
        "Remember: respond in strict JSON."
    )

    return [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": system_prompt}
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": screenshot_data_url}
                },
                {
                    "type": "text",
                    "text": user_instruction
                }
            ]
        }
    ]


def evaluate_completion(client: OpenAI, task: str, screenshot_path: str) -> Dict[str, Any]:
    """
    - Encode screenshot
    - Build evaluation prompt
    - Call GPT-4o (vision-capable)
    - Parse the JSON it returns
    """
    screenshot_b64url = encode_image_to_data_url(screenshot_path)
    messages = build_eval_messages(task, screenshot_b64url)

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.0,
        max_tokens=200,
    )

    raw_text = resp.choices[0].message.content.strip()
    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        result = {
            "completed": None,
            "reason": f"Could not parse as JSON. Raw output was: {raw_text}"
        }

    result["task"] = task
    result["screenshot_path"] = screenshot_path
    result["evaluated_at"] = datetime.utcnow().isoformat() + "Z"

    return result



def main(session_dir: str):

    session_info = load_session_data(session_dir)
    task = session_info["task"]
    screenshot_path = session_info["screenshot_path"]

    client = init_eval_client()
    result = evaluate_completion(client, task, screenshot_path)

    print("\nEvaluation result:")
    print(json.dumps(result, indent=2))

    out_path = Path(session_dir) / "evaluation.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved evaluation to {out_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: python evaluator.py sessions/2025-11-01_18-42-03"
        )
    main(sys.argv[1])
