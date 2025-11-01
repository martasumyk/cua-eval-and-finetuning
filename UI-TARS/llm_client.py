from openai import OpenAI
from typing import List, Dict, Any
from config import HF_BASE_URL, HF_TOKEN, MODEL_ID, build_instruction


def init_client() -> OpenAI:
    return OpenAI(
        base_url=HF_BASE_URL,
        api_key=HF_TOKEN,
    )


def build_messages(task: str, history: List[Dict[str, str]], screenshot_b64: str) -> list[dict]:

    user_turn = {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {"url": screenshot_b64}
            },
            {
                "type": "text",
                "text": build_instruction(task)
            }
        ]
    }

    msgs = [user_turn] + history
    return msgs


def query_model(client: OpenAI, messages: list[dict]) -> str:
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        temperature=0.0,
        max_tokens=400,
        stream=False
    )

    return completion.choices[0].message.content
