from typing import Any

import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration

from .common import (
    SYSTEM_PROMPT,
    build_user_prompt,
    extract_json_object,
    finalize_result,
    load_image_rgb,
)


class LlavaEvaluator:
    def __init__(self, model: str = "llava-hf/llava-1.5-7b-hf"):
        self.model_name = model
        self.processor = AutoProcessor.from_pretrained(self.model_name)
        self.model = LlavaForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True,
            device_map="auto",
        )
        self.device = next(self.model.parameters()).device

    def evaluate(self, task: str, screenshot_path: str) -> dict[str, Any]:
        image = load_image_rgb(screenshot_path)
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"{build_user_prompt(task)}"
        )
        full_prompt = f"USER: <image>\n{prompt}\nASSISTANT:"
        inputs = self.processor(
            text=full_prompt,
            images=image,
            return_tensors="pt",
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.inference_mode():
            generated = self.model.generate(
                **inputs,
                max_new_tokens=200,
                do_sample=False,
            )

        prompt_len = inputs["input_ids"].shape[1]
        generated_ids = generated[:, prompt_len:]
        raw_text = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0].strip()

        result = extract_json_object(raw_text)
        return finalize_result(
            result,
            task=task,
            screenshot_path=screenshot_path,
            evaluator_name="llava",
            model_name=self.model_name,
        )
