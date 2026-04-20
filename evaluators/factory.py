from .anthropic_evaluator import AnthropicEvaluator
from .internvl2_evaluator import InternVL2Evaluator
from .llava_evaluator import LlavaEvaluator
from .openai_evaluator import OpenAIEvaluator
from .qwen2_vl_evaluator import Qwen2VLEvaluator


def create_evaluator(name: str):
    """
    Factory method for creating evaluator objects.
    """
    key = name.strip().lower()

    if key in {"openai", "gpt4o", "gpt-4o"}:
        return OpenAIEvaluator()

    if key in {"anthropic", "claude", "claude3.5", "claude-3.5-sonnet"}:
        return AnthropicEvaluator()

    if key in {"llava", "llava-v1.5-7b", "llava-1.5-7b"}:
        return LlavaEvaluator()

    if key in {"qwen", "qwen2-vl", "qwen2-vl-7b", "qwen2-vl-7b-instruct"}:
        return Qwen2VLEvaluator()

    if key in {"internvl", "internvl2", "internvl2-8b"}:
        return InternVL2Evaluator()

    raise ValueError(f"Unknown evaluator: {name}")
