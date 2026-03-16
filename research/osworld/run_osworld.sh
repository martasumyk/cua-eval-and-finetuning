#!/usr/bin/env bash
set -euo pipefail

cd "${OSWORLD_REPO:-./external/OSWorld}"

python run.py \
  --provider_name docker \
  --headless \
  --observation_type screenshot \
  --model openclaw \
  --sleep_after_execution 3 \
  --max_steps 15 \
  --result_dir ./results/openclaw_osworld \
  --client_password password