# Research on the OpenClaw Model

In this directory, we evaluate the quality of the open-source **OpenClaw** model ([OpenClaw](https://openclaw.ai/)) on three benchmarks used in this work:

- macOSWorld
- OSWorld (Linux)
- Windows Agent Arena

The goal of this analysis is to assess the performance and generalization across operating systems of OpenClaw and compare with our implementation.

## Setup

Install the research-specific dependencies:

```
pip install -r research/requirements.txt
```

Then, create the `.env` file. Example:

```
OPENCLAW_BASE_URL=http://127.0.0.1:3000
OPENCLAW_API_KEY=
OPENCLAW_MODEL=

OSWORLD_REPO=/absolute/path/to/OSWorld
MACOSWORLD_REPO=/absolute/path/to/macosworld
WAA_REPO=/absolute/path/to/WindowsAgentArena
```

## Running the Evaluation

To run all benchmark evaluations from the repository root:

```
python -m research.run_all
```

To run a single benchmark separately:

```
python -m research.macosworld.run_macosworld
python -m research.windows_agent_arena.run_waa
bash research/osworld/run_osworld.sh
```

## Output

Evaluation outputs, logs, trajectories, and benchmark-specific results are stored in:

```
research/results/
```

Each benchmark writes its results into a separate subdirectory.