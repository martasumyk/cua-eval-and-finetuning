import ast
import time
from io import BytesIO

import torch
import pyautogui
from PIL import Image, ImageDraw
from qwen_vl_utils import process_vision_info
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor


def draw_point(image_input, point=None, radius=10, save_path=None):
    """
    Draw a red dot at normalized coords [x, y] on the image.
    point is in [0,1] x [0,1] coordinates.
    """
    print("[draw_point] Called with point:", point)
    if isinstance(image_input, str):
        print("[draw_point] Loading image from path:", image_input)
        image = Image.open(image_input)
    else:
        print("[draw_point] Using provided PIL image object.")
        image = image_input

    if point is not None:
        x, y = point[0] * image.width, point[1] * image.height
        print(f"[draw_point] Drawing point at pixel coords: ({x}, {y})")
        draw = ImageDraw.Draw(image)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="red")
    else:
        print("[draw_point] No point provided; skipping drawing.")

    if save_path:
        image.save(save_path)
        print("[draw_point] Saved visualization:", save_path)
    else:
        print("[draw_point] Showing image on screen.")
        image.show()


# ================== System prompt ================== #
SYSTEM = (
    "You are a computer-use assistant. "
    "Given a high-level task and a screenshot of the screen, "
    "you must output the coordinates of the single NEXT clickable location "
    "to make progress on the task. "
    "The coordinate is a Python list [x, y] with both values in [0, 1], "
    "where x and y are relative to the screenshot width and height. "
    "Respond ONLY with the list, e.g. [0.42, 0.77], with no extra text."
)


# ================== Core model call ================== #
def get_next_click_coords(task, img_path, model, processor, device, min_pixels, max_pixels):
    """
    Given a high-level task and a screenshot, ask ShowUI for the next click location.
    Returns [x, y] in normalized coordinates or None if parsing fails.
    """
    print("[get_next_click_coords] START")
    print("[get_next_click_coords] Task:", task)
    print("[get_next_click_coords] Image path:", img_path)

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

    print("[get_next_click_coords] A: Before apply_chat_template")
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    print("[get_next_click_coords] B: After apply_chat_template")
    # print("[get_next_click_coords] Chat template text:", text)

    print("[get_next_click_coords] C: Before process_vision_info")
    img_inputs, vid_inputs = process_vision_info(messages)
    print("[get_next_click_coords] D: After process_vision_info")
    # Debug shapes if available
    try:
        if img_inputs and hasattr(img_inputs[0], "size"):
            print("[get_next_click_coords] Image input size:", img_inputs[0].size)
    except Exception as e:
        print("[get_next_click_coords] Could not inspect img_inputs:", e)

    print("[get_next_click_coords] E: Before processor(...) for inputs")
    inputs = processor(
        text=[text],
        images=img_inputs,
        videos=vid_inputs,
        padding=True,
        return_tensors="pt",
    ).to(device)
    print("[get_next_click_coords] F: After processor(...) for inputs")
    print("[get_next_click_coords] Input tensor shapes:",
          {k: v.shape for k, v in inputs.items() if hasattr(v, "shape")})

    # CPU inference
    print("[get_next_click_coords] G: Before model.generate")
    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=64)
    print("[get_next_click_coords] H: After model.generate")

    print("[get_next_click_coords] I: Before extracting new tokens")
    new_tokens = [o[len(i):] for i, o in zip(inputs.input_ids, out)]
    print("[get_next_click_coords] J: After extracting new tokens")

    print("[get_next_click_coords] K: Before batch_decode")
    output = processor.batch_decode(
        new_tokens,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]
    print("[get_next_click_coords] L: After batch_decode")

    print("[get_next_click_coords] Model raw output:", repr(output))

    try:
        print("[get_next_click_coords] M: Before ast.literal_eval")
        xy = ast.literal_eval(output)
        print("[get_next_click_coords] N: After ast.literal_eval, parsed:", xy)
        if (
            isinstance(xy, (list, tuple))
            and len(xy) == 2
            and all(isinstance(v, (int, float)) for v in xy)
        ):
            print("[get_next_click_coords] Parsed coords OK:", xy)
            print("[get_next_click_coords] END (success)")
            return xy
        else:
            print("[get_next_click_coords] Output is not a simple [x, y] list.")
            print("[get_next_click_coords] END (invalid format)")
            return None
    except Exception as e:
        print("[get_next_click_coords] Could not parse output with ast.literal_eval:", e)
        print("[get_next_click_coords] END (parse error)")
        return None


# ================== Agent utilities ================== #
def take_screenshot(path="screen.png"):
    """
    Take a screenshot of the main screen and save it as a PNG.
    """
    print("[take_screenshot] START: saving to", path)
    img = pyautogui.screenshot()
    print("[take_screenshot] Screenshot taken. Size:", img.size)
    img.save(path)
    print("[take_screenshot] Screenshot saved.")
    print("[take_screenshot] END")
    return path


def click_normalized(xy, move_duration=0.2):
    """
    Convert normalized [x, y] coords to absolute screen coords and click.
    """
    print("[click_normalized] START with xy:", xy)
    screen_w, screen_h = pyautogui.size()
    print("[click_normalized] Screen size:", (screen_w, screen_h))

    x_abs = int(xy[0] * screen_w)
    y_abs = int(xy[1] * screen_h)

    print(f"[click_normalized] Clicking at screen coords: ({x_abs}, {y_abs})")
    pyautogui.moveTo(x_abs, y_abs, duration=move_duration)
    pyautogui.click()
    print("[click_normalized] Click done.")
    print("[click_normalized] END")


# ================== Main agent loop ================== #
def main():
    print("[main] START")
    # High-level task
    task = input("Enter your task for the agent (e.g. 'open gmail in browser and log in'): ")
    print("[main] Task entered:", task)

    # Safety: let you abort by moving mouse to top-left corner
    pyautogui.FAILSAFE = True
    print("[main] pyautogui.FAILSAFE set to True")

    # CPU-only config
    device = "cpu"
    torch_dtype = torch.float32
    print("[main] Using device:", device, "dtype:", torch_dtype)

    # ShowUI image size constraints
    min_pixels = 256 * 28 * 28
    max_pixels = 1344 * 28 * 28
    print("[main] min_pixels:", min_pixels, "max_pixels:", max_pixels)

    # Load model + processor on CPU
    print("[main] Loading model...")
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        "showlab/ShowUI-2B",
        torch_dtype=torch_dtype,   # will show deprecation warning, but ok
        device_map=None,
    ).to(device)
    print("[main] Model loaded and moved to device.")

    print("[main] Loading processor...")
    processor = AutoProcessor.from_pretrained(
        "showlab/ShowUI-2B",
        min_pixels=min_pixels,
        max_pixels=max_pixels,
    )
    print("[main] Processor loaded.")

    print("[main] Model & processor ready. Starting agent loop.")
    print("[main] Move your mouse to the top-left corner of the screen to abort (pyautogui FAILSAFE).")

    # How many steps to attempt automatically
    max_steps = 10
    print("[main] max_steps:", max_steps)

    for step in range(1, max_steps + 1):
        print(f"\n[main] === Step {step}/{max_steps} ===")

        # 1) Screenshot current screen
        img_path = "screen.png"
        print("[main] A: Before screenshot")
        img_path = take_screenshot(img_path)
        print("[main] B: After screenshot, image saved at", img_path)

        # 2) Ask ShowUI where to click next
        print("[main] C: Before get_next_click_coords")
        xy = get_next_click_coords(
            task=task,
            img_path=img_path,
            model=model,
            processor=processor,
            device=device,
            min_pixels=min_pixels,
            max_pixels=max_pixels,
        )
        print("[main] D: After get_next_click_coords, xy:", xy)

        if xy is None:
            print("[main] Stopping: could not get valid coordinates.")
            break

        # Optional: visualize prediction for debugging
        # print("[main] Visualizing predicted click...")
        # draw_point(img_path, xy, save_path=f"vis_step_{step}.png")

        # 3) Execute click
        print("[main] E: Before click_normalized")
        click_normalized(xy)
        print("[main] F: After click_normalized")

        # 4) Short pause so UI can update
        print("[main] Sleeping 1.5 seconds to let UI update...")
        time.sleep(1.5)

    print("[main] Agent loop finished.")
    print("[main] END")


if __name__ == "__main__":
    main()
