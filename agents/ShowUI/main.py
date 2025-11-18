import ast
import time
from io import BytesIO

import torch
import pyautogui
from PIL import Image, ImageDraw
from qwen_vl_utils import process_vision_info
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor


SYSTEM = (
    "You are a computer-use assistant. "
    "Given a high-level task and a screenshot of the screen, "
    "you must output the coordinates of the single NEXT clickable location "
    "to make progress on the task. "
    "The coordinate is a Python list [x, y] with both values in [0, 1], "
    "where x and y are relative to the screenshot width and height. "
    "Respond ONLY with the list, e.g. [0.42, 0.77], with no extra text."
)


def get_next_click_coords(task, img_path, model, processor, device, min_pixels, max_pixels):

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": SYSTEM},
                {
                    "type": "image",
                    "image": img_path,
                    "min_pixels": min_pixels,
                    "max_pixels": max_pixels,
                },
                {"type": "text", "text": f"Task: {task}"},
            ],
        }
    ]

    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )


    img_inputs, vid_inputs = process_vision_info(messages)


    inputs = processor(
        text=[text],
        images=img_inputs,
        videos=vid_inputs,
        padding=True,
        return_tensors="pt",
    ).to(device)


    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=64)

    new_tokens = [o[len(i):] for i, o in zip(inputs.input_ids, out)]

    output = processor.batch_decode(
        new_tokens,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]


    try:
        xy = ast.literal_eval(output)

        if (
            isinstance(xy, (list, tuple))
            and len(xy) == 2
            and all(isinstance(v, (int, float)) for v in xy)
        ):


            return xy
        else:

            return None
    except Exception as e:

        return None


def take_screenshot(path="screen.png"):
    """
    Take a screenshot of the main screen and save it as a PNG.
    """
    img = pyautogui.screenshot()
    img.save(path)
    return path


def click_normalized(xy, move_duration=0.2):
    """
    Convert normalized [x, y] coords to absolute screen coords and click.
    """
    screen_w, screen_h = pyautogui.size()

    x_abs = int(xy[0] * screen_w)
    y_abs = int(xy[1] * screen_h)

    pyautogui.moveTo(x_abs, y_abs, duration=move_duration)
    pyautogui.click()



# ================== Main agent loop ================== #
def main():
    task = input("Enter your task for the agent: ")

    pyautogui.FAILSAFE = True

    device = "cpu"
    torch_dtype = torch.float32

    min_pixels = 256 * 28 * 28
    max_pixels = 1344 * 28 * 28

    model = Qwen2VLForConditionalGeneration.from_pretrained(
        "showlab/ShowUI-2B",
        torch_dtype=torch_dtype, 
        device_map=None,
    ).to(device)


    processor = AutoProcessor.from_pretrained(
        "showlab/ShowUI-2B",
        min_pixels=min_pixels,
        max_pixels=max_pixels,
    )

    max_steps = 10
    print("[main] max_steps:", max_steps)

    for step in range(1, max_steps + 1):
        print(f"\nStep {step}/{max_steps}")

        img_path = "screen.png"

        img_path = take_screenshot(img_path)

        xy = get_next_click_coords(
            task=task,
            img_path=img_path,
            model=model,
            processor=processor,
            device=device,
            min_pixels=min_pixels,
            max_pixels=max_pixels,
        )

        if xy is None:
            break

        click_normalized(xy)

        time.sleep(0.5)



if __name__ == "__main__":
    main()
