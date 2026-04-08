import os
import random
from openai import OpenAI
from env.waste_env import WasteEnv

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN is required")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

random.seed(42)

def fallback(state):
    return 2 if state["waste_type"] == "organic" else 1

def get_action(state):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                "content": f"{state}. Return only a number 0-3."
            }]
        )
        return response.choices[0].message.content.strip()
    except:
        return str(fallback(state))

def run(task):
    env = WasteEnv(task)
    state = env.reset()

    print(f"[START] task={task} env=waste_env model={MODEL_NAME}")

    rewards = []
    success = False

    for step in range(1, 11):
        error = None

        try:
            action_str = get_action(state)
            action = int(action_str)
            state, reward, done, _ = env.step(action)

        except Exception as e:
            reward = 0.0
            done = True
            error = str(e)
            action_str = "invalid"

        rewards.append(f"{reward:.2f}")

        print(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={str(done).lower()} error={error if error else 'null'}")

        if done:
            success = reward > 0
            break

    score = sum(float(r) for r in rewards) / len(rewards)

    print(f"[END] success={str(success).lower()} steps={step} score={score:.2f} rewards={','.join(rewards)}")
if __name__ == "__main__":
    for t in ["easy", "medium", "hard"]:
        run(t)