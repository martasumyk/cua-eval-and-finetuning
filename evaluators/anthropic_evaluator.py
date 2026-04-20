import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from .common import (
    SYSTEM_PROMPT,
    build_user_prompt,
    encode_image_to_data_url,
    extract_json_object,
    finalize_result,
)


class OpenAIEvaluator:
    def __init__(self, model: str | None = None):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment / .env")
        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_EVALUATOR_MODEL", "gpt-4o")

    def evaluate(self, task: str, screenshot_path: str) -> dict[str, Any]:
        image_url = encode_image_to_data_url(screenshot_path)
        response = self.client.responses.create(
            model=self.model,
            temperature=0,
            max_output_tokens=200,
            input=[
                {
                    "role": "system",
                    "content": [
                        {"type": "input_text", "text": SYSTEM_PROMPT},
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": build_user_prompt(task)},
                        {"type": "input_image", "image_url": image_url},
                    ],
                },
            ],
        )
        raw_text = response.output_text.strip()
        result = extract_json_object(raw_text)
        return finalize_result(
            result,
            task=task,
            screenshot_path=screenshot_path,
            evaluator_name="openai",
            model_name=self.model,
        )
