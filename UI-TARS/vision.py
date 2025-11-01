import io
import base64
import re
import mss
from PIL import Image

def take_screenshot_b64() -> str:
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        raw = sct.grab(monitor)
        img = Image.frombytes("RGB", raw.size, raw.rgb)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return "data:image/png;base64," + b64


def add_box_token(text: str) -> str:
    if "Action:" in text and "start_box=" in text:
        prefix = text.split("Action: ")[0] + "Action: "
        actions = text.split("Action: ")[1:]
        out_parts = []

        for a in actions:
            a = a.strip()
            coords = re.findall(r"(start_box|end_box)='\((\d+),\s*(\d+)\)'", a)
            upd = a

            for coord_type, x, y in coords:
                old = f"{coord_type}='({x},{y})'"
                new = f"{coord_type}='<|box_start|>({x},{y})<|box_end|>'"
                upd = upd.replace(old, new)

            out_parts.append(upd)
        return prefix + "\n\n".join(out_parts)

    return text
