# Rum UTM VM

Here we present a lightweight Python module for controlling [UTM](https://docs.getutm.app/advanced/remote-control/) virtual machines on macOS via URL commands. This is used to controll experiments, performed in the thesis.

> **macOS only** — UTM automation relies on `open utm://...` URLs, which are available on macOS exclusively.

## Table of Contents

- [Commands](#commands)
- [Usage](#usage)
- [Configuration](#configuration)
- [Python API](#python-api)
- [Reference](#reference)

## Commands

| Command | Description |
|---|---|
| `start` | Start the VM |
| `stop` | Stop the VM |
| `restart` | Restart the VM |
| `pause` | Pause the VM |
| `resume` | Resume a paused VM |
| `send-text` | Send text as keystrokes to the VM |
| `click` | Click inside the VM window at pixel coordinates |

## Usage

```bash
# Start the VM (waits 30s by default)
python -m run_vm start

# Start and wait 60 seconds
python -m run_vm start --wait 60

# Stop the VM
python -m run_vm stop

# Restart with a 20-second wait
python -m run_vm restart --wait 20

# Pause / resume
python -m run_vm pause
python -m run_vm resume

# Send text as keystrokes
python -m run_vm send-text "hello world"

# Click at coordinates (left button by default)
python -m run_vm click --x 400 --y 300

# Click with a specific mouse button
python -m run_vm click --x 400 --y 300 --button right

# Target a specific VM by name
python -m run_vm --vm-name "My VM" start
```

## Configuration

Edit `config.py` to set defaults:

```python
VM_NAME = "UTM VM"           # Name of the VM as it appears in UTM
DEFAULT_START_WAIT = 30      # Seconds to wait after start/restart
DEFAULT_WAKE_CLICK = None    # Optional (x, y) coords to click after start
```

## Python API

You can also import and use the functions directly:

```python
from run_vm.utm_vm import start_vm, stop_vm, send_text, click_in_vm

start_vm(vm_name="UTM VM", wait=30)
send_text("hello", vm_name="UTM VM")
click_in_vm(x=400, y=300, button="left", vm_name="UTM VM")
stop_vm(vm_name="UTM VM")
```

## Reference

- [UTM Remote Control Docs](https://docs.getutm.app/advanced/remote-control/)
