from transformers import AutoTokenizer, AutoModelForCausalLM
from trl import PPOTrainer, PPOConfig
from datasets import Dataset
from rl_tuning.rollout_env import collect_rollout
import torch, json, os

MODEL_DIR = "ByteDance-Seed/UI-TARS-1.5-7B"
OUTPUT_DIR = "ppo_finetuned"

ppo_config = PPOConfig(
    model_name=MODEL_DIR,
    learning_rate=1e-6,
    batch_size=1,
    mini_batch_size=1,
    gradient_accumulation_steps=1,
    log_with=None,
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, torch_dtype=torch.bfloat16)

trainer = PPOTrainer(config=ppo_config, model=model, tokenizer=tokenizer)

tasks = [
    "Open System Settings and enable Night Shift.",
    "Open Safari and go to apple.com.",
]

rollouts = []
for task in tasks:
    rollout = collect_rollout(task)
    rollouts.append(rollout)
    print(f"{task} -> reward {rollout['reward']}")

texts, rewards = [], []
for r in rollouts:
    session_dir = r["session_dir"]
    log_path = os.path.join(session_dir, "session_log.json")
    with open(log_path) as f:
        data = json.load(f)

    traj_text = "\n".join(step["model_reply"] for step in data["steps"])
    texts.append(traj_text)
    rewards.append(r["reward"])

dataset = Dataset.from_dict({"query": texts, "response": texts, "reward": rewards})

for sample in dataset:
    query_tensors = tokenizer(sample["query"], return_tensors="pt").input_ids
    response_tensors = tokenizer(sample["response"], return_tensors="pt").input_ids
    r = torch.tensor([sample["reward"]], dtype=torch.float32)
    stats = trainer.step([query_tensors[0]], [response_tensors[0]], r)
    print("Step stats:", stats)

trainer.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
