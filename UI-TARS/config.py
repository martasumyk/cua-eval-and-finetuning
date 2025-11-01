import os
from dotenv import load_dotenv

load_dotenv()

HF_BASE_URL = os.getenv("HF_BASE_URL")
HF_TOKEN    = os.getenv("HF_TOKEN")
MODEL_ID    = os.getenv("MODEL_ID", "ByteDance-Seed/UI-TARS-1.5-7B")

TASK        = "Open System Settings and enable Night Shift."

PROMPT_TEMPLATE = """You are a GUI agent. You are given a task and your action history, with screenshots. You need to perform the next action to complete the task.

## Output Format
Thought: ...
Action: ...

## Action Space
click(point='<point>x1 y1</point>')
left_double(point='<point>x1 y1</point>')
right_single(point='<point>x1 y1</point>')
drag(start_point='<point>x1 y1</point>', end_point='<point>x2 y2</point>')
hotkey(key='ctrl c')
type(content='xxx')
scroll(point='<point>x1 y1</point>', direction='down or up or right or left')
wait()
finished(content='xxx')

## Note
- Use English in `Thought` part.
- Write a small plan and finally summarize your next action (with its target element) in one sentence in `Thought` part.

## User Instruction
{instruction}
"""

def build_instruction(task: str) -> str:
    """Fill the prompt template with the current task."""
    return PROMPT_TEMPLATE.format(instruction=task)
