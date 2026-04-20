import subprocess


def run(cmd):
    print(">>>", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    run(["python", "-m", "research.macosworld.run_macosworld"])
    run(["python", "-m", "research.windows_agent_arena.run_waa"])
    run(["bash", "research/osworld/run_osworld.sh"])


if __name__ == "__main__":
    main()
