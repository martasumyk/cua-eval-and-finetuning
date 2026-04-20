import subprocess

from research.config import RESULTS_DIR, WAA_REPO


def main():
    out_dir = RESULTS_DIR / "openclaw_waa"
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python",
        "run.py",
        "--agent",
        "openclaw",
        "--result_dir",
        str(out_dir),
    ]
    subprocess.run(cmd, cwd=WAA_REPO, check=True)


if __name__ == "__main__":
    main()
