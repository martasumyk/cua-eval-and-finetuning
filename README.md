# Reinforcement Learning with Autonomous Feedback for Computer Use Agents

This repository contains the code accompanying the thesis **“Reinforcement Learning with Autonomous Feedback for Computer Use Agents.”** The project investigates how autonomous evaluator signals, produced by Vision-Language Models, can be used to assess task completion and support reinforcement learning for Computer Use Agents operating in desktop environments.

## Overview

### Research Questions

- Can Vision-Language Models (VLMs) serve as effective autonomous evaluators of task completion for computer-use agents operating in real-world desktop environments?
- How can noisy autonomous evaluation signals be incorporated as reward feedback for reinforcement learning fine-tuning of CUAs in a statistically principled and robust manner?

## Structure

```
├── agents/         # Agents implementations and related utilities
├── evaluators/     # Autonomous evaluator models, prompts, and evaluation code
├── research/       # Research scripts for evaluating OpenClaw
├── rl_tuning/      # Reinforcement learning fine-tuning pipeline
├── run_vm/         # Code for running experiments in virtual machine (UTM) environment
├── .flake8         # Linting configuration
├── Makefile        # Commands for setting up linter
├── README.md       # Project documentation
├── datasheet.md    # Dataset documentation
├── pyproject.toml  # Project configuration
└── requirements.txt # Python dependencies
```




## Data

The dataset is available at Zenodo [link placeholder].



