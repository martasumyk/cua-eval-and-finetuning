import subprocess
import sys
import time
import urllib.parse
from typing import Optional, Tuple

from .config import VM_NAME, DEFAULT_START_WAIT


def _ensure_macos():
    """
    Check to insure the current OS is macOS.
    """
    if sys.platform != "darwin":
        raise RuntimeError("UTM automation only works on macOS (sys.platform == 'darwin').")


def _utm_url(command: str, **params) -> str:
    query = urllib.parse.urlencode(params)
    return f"utm://{command}?{query}"


def _open_url(url: str) -> None:
    _ensure_macos()
    subprocess.run(["open", url], check=True)



def start_vm(vm_name: str = VM_NAME, wait: Optional[int] = DEFAULT_START_WAIT) -> None:
    """
    Start the VM by name.
    """
    url = _utm_url("start", name=vm_name)
    _open_url(url)

    if wait and wait > 0:
        time.sleep(wait)


def stop_vm(vm_name: str = VM_NAME) -> None:
    """
    Stop the VM immediately.
    """
    url = _utm_url("stop", name=vm_name)
    _open_url(url)


def restart_vm(vm_name: str = VM_NAME, wait: Optional[int] = DEFAULT_START_WAIT) -> None:
    """
    Restart the VM (stop -> start).
    """
    url = _utm_url("restart", name=vm_name)
    _open_url(url)

    if wait and wait > 0:
        time.sleep(wait)


def pause_vm(vm_name: str = VM_NAME) -> None:
    url = _utm_url("pause", name=vm_name)
    _open_url(url)


def resume_vm(vm_name: str = VM_NAME) -> None:
    url = _utm_url("resume", name=vm_name)
    _open_url(url)



def send_text(text: str, vm_name: str = VM_NAME) -> None:
    """
    Type text into the VM as if from the keyboard.
    """
    url = _utm_url("sendText", name=vm_name, text=text)

    _open_url(url)


def click_in_vm(x: int, y: int, button: str = "left", vm_name: str = VM_NAME) -> None:
    """
    Click inside the VM at pixel coordinates (x, y) within the VM window.
    """
    url = _utm_url("click", name=vm_name, x=str(x), y=str(y), button=button)

    _open_url(url)


def wake_vm(vm_name: str = VM_NAME, coords: Optional[Tuple[int, int]] = None) -> None:
    """
    Optional helper: perform a small click to 'wake up' or unlock screen.

    """
    if coords is None:

        return

    x, y = coords
    click_in_vm(x, y, vm_name=vm_name)
