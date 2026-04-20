# Reinforcement Learning Fine-Tuning

Reinforcement learning fine-tuning module for Computer Use Agents (CUAs). Implements a PPO-based training loop with an autonomous task-completion evaluator and noise-aware reward correction.

## Pipeline

The framework operates as a closed loop:
1. The **Computer Use Agent** perceives the desktop state $s_t$ and executes actions $a_t$.
2. After each episode, the final screenshot $s_{i,n}$ is passed to the **Autonomous Evaluator**, which produces a noisy binary reward $\tilde{r}_i$.
3. A **noise-aware correction** converts $\tilde{r}_i$ into a calibrated reward $\hat{r}_i = f(\tilde{r}_i)$.
4. The corrected reward is used in a **PPO update** $\theta \leftarrow \theta + \nabla_\theta J(\theta)$.

## File Structure

```
rl_tuning/
├── __init__.py           # Public API exports
├── collect_rollout.py    # Runs a single episode and returns a rollout dict
├── rollout_env.py        # Desktop environment: screenshot → policy → action loop
├── logprobs.py           # Sequence log-probability computation for PPO
├── rewards.py            # Noise-aware Bayesian reward correction
└── trainer.py            # PPO training loop (entry point)
```

## Reward Correction

The autonomous evaluator is modeled with two noise parameters:

| Parameter | Symbol | Description |
|---|---|---|
| False positive rate | α | P(evaluator says complete \| task incomplete) |
| False negative rate | β | P(evaluator says incomplete \| task complete) |

The corrected reward is computed via Bayes' theorem:

```
P(complete | r̃=1) = (1 - β) · p  /  [(1 - β) · p + α · (1 - p)]
```

where `p` is the prior probability of task success.

## Usage

### Run PPO training

```bash
python -m rl_tuning.trainer
```

### Collect a single rollout

```python
from rl_tuning import collect_rollout, EvaluatorNoiseParams

noise = EvaluatorNoiseParams(false_positive_rate=0.1, false_negative_rate=0.15)

rollout = collect_rollout(
    task="Open Safari and go to apple.com.",
    model=model,
    tokenizer=tokenizer,
    noise=noise,
)

print(rollout["reward"])               # corrected scalar reward
print(rollout["evaluator_completed"])  # raw evaluator signal (0 or 1)
print(rollout["evaluator_justification"])
```

### Compute corrected reward manually

```python
from rl_tuning.rewards import EvaluatorNoiseParams, compute_episode_reward

noise = EvaluatorNoiseParams(false_positive_rate=0.1, false_negative_rate=0.1)
reward = compute_episode_reward(evaluator_completed=1, noise=noise, prior_success=0.5)
```

## Configuration

Key parameters are set at the top of `trainer.py`:

| Variable | Default | Description |
|---|---|---|
| `MODEL_DIR` | `ByteDance-Seed/UI-TARS-1.5-7B` | Base model path |
| `OUTPUT_DIR` | `ppo_finetuned` | Output directory for fine-tuned weights |
| `learning_rate` | `1e-6` | PPO learning rate |
| `batch_size` | `1` | PPO batch size |

## Dependencies

- `transformers` — model loading and tokenization
- `trl` — PPO trainer
- `torch` — tensor operations and log-probability computation
- `datasets` — rollout dataset construction