import base64
from pathlib import Path


def image_to_base64(image_path: str | Path) -> str:
    image_path = Path(image_path)
    with image_path.open("rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")