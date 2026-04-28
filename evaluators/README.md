# Evaluators

This directory contains the autonomous evaluators used in the thesis for judging whether a Computer Use Agent has successfully completed a task. Each evaluator receives the task description together with the final screenshot of the environment and returns a structured judgement in JSON format.

The goal of these evaluators is to provide an automatic success signal that can be used for:
- standalone evaluation of task completion
- comparison of different evaluator models
- feedback for reinforcement learning fine-tuning

## Table of Contents

- [Supported Evaluators](#supported-evaluators)
- [Directory Structure](#directory-structure)
- [Input Format](#input-format)
- [Usage](#usage)
- [Environment Setup](#environment-setup)
- [Evaluator Design](#evaluator-design)

## Supported evaluators

The following evaluator backends are implemented in this directory:

- **OpenAI GPT-4o**
- **Anthropic Claude**
- **LLaVA-v1.5-7B**
- **Qwen2-VL-7B**
- **InternVL2-8B**

These evaluators include both API-based models and open-weight vision-language models.

## Directory structure

```text
evaluators/
├── __init__.py
├── common.py
├── factory.py
├── run_evaluator.py
├── openai_evaluator.py
├── anthropic_evaluator.py
├── llava_evaluator.py
├── qwen2_vl_evaluator.py
├── internvl2_evaluator.py
└── README.md
```

## Input format

Each evaluator expects a session directory containing a session_log.json file with task metadata and step information. The evaluator reads:

- the task description
- the final step
- the screenshot path from the final step


## Usage 

You can run any supported evaluator with the shared entry point:

```
python -m evaluators.run_evaluator openai path/to/session
python -m evaluators.run_evaluator claude path/to/session
python -m evaluators.run_evaluator llava path/to/session
python -m evaluators.run_evaluator qwen2-vl path/to/session
python -m evaluators.run_evaluator internvl2 path/to/session
```

## Environment setup

Some evaluators require API keys, while others run locally from Hugging Face checkpoints.

Create a `.env` file in the project root with the required variables:

```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_EVALUATOR_MODEL=gpt-4o
ANTHROPIC_MODEL=claude-sonnet-4-6
```


If you only use a subset of evaluators, you only need to provide the corresponding variables.


## Evaluator design

All evaluators follow the same high-level procedure:

1. Load the task and the final screenshot from the session directory.
2. Construct an evaluation prompt asking whether the task is completed.
3. Run the selected vision-language model.
4. Parse the model output into a strict JSON judgement.
5. Save the final result.

This shared design makes it possible to compare different evaluator models under a unified interface.
