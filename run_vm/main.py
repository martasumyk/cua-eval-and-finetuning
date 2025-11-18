"""
Examples of commands:

    python -m run_vm start
    python -m run_vm stop
    python -m run_vm restart --wait 20
    python -m run_vm send-text "niiiiiceee"
    python -m run_vm click --x 400 --y 300
"""

import argparse

from .config import VM_NAME, DEFAULT_START_WAIT
from .utm_vm import (
    start_vm,
    stop_vm,
    restart_vm,
    pause_vm,
    resume_vm,
    send_text,
    click_in_vm,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run_vm", description="Control a UTM VM from Python.")
    parser.add_argument(
        "--vm-name",
        default=VM_NAME,
        help=f"Name of the VM in UTM (default: {VM_NAME!r})",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="Start the VM.")
    p_start.add_argument(
        "--wait",
        type=int,
        default=DEFAULT_START_WAIT,
        help=f"Seconds to wait after start (default: {DEFAULT_START_WAIT}). Set 0 to skip.",
    )

    sub.add_parser("stop", help="Stop the VM.")

    p_restart = sub.add_parser("restart", help="Restart the VM.")
    p_restart.add_argument(
        "--wait",
        type=int,
        default=DEFAULT_START_WAIT,
        help=f"Seconds to wait after restart (default: {DEFAULT_START_WAIT}). Set 0 to skip.",
    )

    # pause / resume
    sub.add_parser("pause", help="Pause the VM.")
    sub.add_parser("resume", help="Resume a paused VM.")

    # send text
    p_text = sub.add_parser("send-text", help="Send text as keystrokes to the VM.")
    p_text.add_argument("text", help="The text to send.")

    # click (left/right/middle)
    p_click = sub.add_parser("click", help="Click inside VM window at pixel coords.")
    p_click.add_argument("--x", type=int, required=True, help="X pixel coordinate.")
    p_click.add_argument("--y", type=int, required=True, help="Y pixel coordinate.")
    p_click.add_argument(
        "--button",
        choices=["left", "middle", "right"],
        default="left",
        help="Mouse button (default: left).",
    )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    vm_name = args.vm_name

    if args.command == "start":
        start_vm(vm_name=vm_name, wait=args.wait)
    elif args.command == "stop":
        stop_vm(vm_name=vm_name)
    elif args.command == "restart":
        restart_vm(vm_name=vm_name, wait=args.wait)
    elif args.command == "pause":
        pause_vm(vm_name=vm_name)
    elif args.command == "resume":
        resume_vm(vm_name=vm_name)
    elif args.command == "send-text":
        send_text(args.text, vm_name=vm_name)
    elif args.command == "click":
        click_in_vm(args.x, args.y, button=args.button, vm_name=vm_name)
    else:
        parser.error(f"Unknown command: {args.command!r}")


if __name__ == "__main__":
    main()
