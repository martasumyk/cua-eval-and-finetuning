# Agents

Here you can see small wrappers around different Computer-Use agents that can control your desktop, log trajectories, and save screenshots:

- `Anthropic_CU/` – runner for the Anthropic Computer Use (CU) agent.
- `UI-TARS/` – runner for a HuggingFace-hosted **UI-TARS** vision-based agent.
- `OpenAI_Operator/` – runner an OpenAI-based operator.


## Installation


```bash
git clone <this-repo-url>
cd <this-repo-dir>

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -U pip
pip install -r requirements.txt
```

Make sure your terminal/IDE has Accessibility and Screen Recording permissions so the agents can control the mouse and capture screenshots.


## Running Agents

### Anthropic CU

Make sure to set Anthropic API key.

Run sigle task from terminal:

```bash

cd Anthropic_CU
python main.py --task "Open System Settings and enable Night Shift." --output_dir trajectories


```

Run tasks from .csv file:

```bash
python main.py --tasks_csv tasks.csv --output_dir trajectories
```

Trajectories will be saved under `trajectories/<app_name>/task_XXX/` with:

- `step_XX.png` screenshots

- `step_XX.json` tool calls + metadata

- `task_XXX.txt` task description

### UI-TARS Agent

Create `.env` in `UI-TARS/`:

```bash
HF_BASE_URL=https://your-endpoint/v1/
HF_TOKEN=hf_xxx
MODEL_ID=ByteDance-Seed/UI-TARS-1.5-7B
```


Run task:

```bash
cd UI-TARS
python main.py
```

### OpenAI Operator

Make sure you set OpenAI API key with the Operator permissions.

Run task:

```bash
cd OpenAI_Operator
python main.py
```