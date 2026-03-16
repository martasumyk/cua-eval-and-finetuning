import subprocess
from research.config import MACOSWORLD_REPO, RESULTS_DIR


def main():
    out_dir = RESULTS_DIR / "openclaw_macosworld"
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python",
        "run.py",
        "--agent",
        "openclaw",
        "--result_dir",
        str(out_dir),
    ]
    subprocess.run(cmd, cwd=MACOSWORLD_REPO, check=True)


if __name__ == "__main__":
    main()