# Reinforcement Learning with Autonomous Feedback for Computer Use Agents

This repository contains the code accompanying the thesis **“Reinforcement Learning with Autonomous Feedback for Computer Use Agents.”** The project investigates how autonomous evaluator signals, produced by Vision-Language Models, can be used to assess task completion and support reinforcement learning for Computer Use Agents operating in desktop environments.

## Overview

### Research Questions

- **RQ1:** Can Vision-Language Models (VLMs) serve as effective autonomous evaluators of task completion for computer-use agents operating in real-world desktop environments?
- **RQ2:** How can noisy autonomous evaluation signals be incorporated as reward feedback for reinforcement learning fine-tuning of CUAs in a statistically principled and robust manner?

### Contributions 



## Repository Structure

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

## Installation 

## Quick Start


## Data

The dataset is available at Zenodo [link placeholder].

## Autonomous Evaluators

## Reinforcement Learning Fine-Tuning

## Publications and Intermediate Projects

This thesis builds on two intermediate research projects focused on autonomous evaluation and auditing for Computer Use Agents.

### 1. *Are We Done Yet?*: A Vision-Based Judge for Autonomous Task Completion of Computer Use Agents  
**Accepted at [AAAI 2026 Workshop on Trust and Control in Agentic AI (TrustAgent)](https://trustagenticai.github.io/AAAI2026/)**

This project studies whether Vision-Language Models can judge task completion for Computer Use Agents directly from screenshots and task descriptions. It introduces a dataset of 1,260 human-labeled tasks across 42 built-in macOS applications and shows that evaluator feedback can improve agent reliability and self-correction.

[![arXiv](https://img.shields.io/badge/arXiv-2511.20067-b31b1b.svg)](https://arxiv.org/abs/2511.20067)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.17696742-blue.svg)](https://doi.org/10.5281/zenodo.17696742)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-Project-00ccbb.svg)](https://www.researchgate.net/publication/397983499_Are_We_Done_Yet_A_Vision-Based_Judge_for_Autonomous_Task_Completion_of_Computer_Use_Agents)

### 2. *CUAAudit*: Meta-Evaluation of Vision-Language Models as Auditors of Autonomous Computer-Use Agents  
**Accepted at [HEAL @ CHI 2026 Workshop on Human-centered Evaluation and Auditing of Language Models](https://heal-workshop.github.io/)**

This project evaluates Vision-Language Models as autonomous auditors of Computer Use Agents across macOS, Windows, and Linux benchmarks. It studies auditor performance in terms of accuracy, calibration, and inter-model agreement, highlighting both the promise and the limitations of model-based task evaluation.

[![arXiv](https://img.shields.io/badge/arXiv-2603.10577-b31b1b.svg)](https://arxiv.org/abs/2603.10577)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-Project-00ccbb.svg)](https://www.researchgate.net/publication/401834043_CUAAudit_Meta-Evaluation_of_Vision-Language_Models_as_Auditors_of_Autonomous_Computer-Use_Agents)
## Citation

To be added.

