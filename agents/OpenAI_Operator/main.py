import argparse
import csv
import json
import os
import re
import time
from typing import Dict, List, Tuple

from openai import OpenAI

AI_WIDTH, AI_HEIGHT = 1024, 768


def slugify_app_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-z0-9_]+", "", name)
    return name or "unknown_app"


def read_tasks_from_csv(path: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task = (row.get("task_description") or row.get("task") or "").strip()
            app = (row.get("app") or "").strip()
            if task:
                rows.append({"task": task, "app": app})
    return rows


def next_task_dir(app_root: str) -> Tuple[str, int]:
    os.makedirs(app_root, exist_ok=True)
    existing = [d for d in os.listdir(app_root) if d.startswith("task_")]
    nums = []
    for d in existing:
        try:
            nums.append(int(d.split("_")[1]))
        except Exception:
            pass
    nxt = (max(nums) + 1) if nums else 1
    name = f"task_{nxt:03d}"
    full = os.path.join(app_root, name)
    os.makedirs(full, exist_ok=True)
    return full, nxt


def run_single_task(client: OpenAI, task_text: str, app_root: str):
    task_dir, task_num = next_task_dir(app_root)
    print(f"\n[{app_root}] Running task {task_num:03d}: {task_text}")

    with open(os.path.join(task_dir,
                           f"task_{task_num:03d}.txt"), "w", encoding="utf-8") as f:
        f.write(task_text)

    response = client.responses.create(
        model="computer-use-preview",
        tools=[
            {
                "type": "computer_use_preview",
                "display_width": AI_WIDTH,
                "display_height": AI_HEIGHT,

                "environment": "desktop",
            }
        ],
        truncation="auto",
        input=task_text,
    )

    out_path = os.path.join(task_dir, f"response_{task_num:03d}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(response.__dict__, f, default=lambda o: o.__dict__, indent=2)

    try:
        if response.output and response.output[0].content:
            text = response.output[0].content[0].text
    except Exception:
        pass
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Run OpenAI computer-use (Operator) over tasks.csv"
    )
    parser.add_argument(
        "--tasks_csv",
        type=str,
        default="tasks.csv",
        help="CSV with columns task_description,app",
    )
    parser.add_argument(
        "--output_root",
        type=str,
        default="openai_operator_runs",
        help="Root directory for logs / trajectories.",
    )
    args = parser.parse_args()

    client = OpenAI()

    tasks = read_tasks_from_csv(args.tasks_csv)
    os.makedirs(args.output_root, exist_ok=True)

    for i, row in enumerate(tasks, start=1):
        task_text = row["task"]
        app_name = row["app"] or "unknown_app"
        app_slug = slugify_app_name(app_name)
        app_root = os.path.join(args.output_root, app_slug)

        print(f"\n=== [{i}/{len(tasks)}] {task_text}  (app={app_name}) ===")
        run_single_task(client, task_text, app_root)
        time.sleep(1)


if __name__ == "__main__":
    main()
