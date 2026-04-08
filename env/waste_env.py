import random
from env.models import Observation

def normalize_score(x):
    # ensures strictly between (0,1)
    return max(0.01, min(0.99, round(x, 2)))

class WasteEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.steps = 0
        self.max_steps = 20

        self.total_cost = 0
        self.total_overflow = 0
        self.correct_actions = 0

        self.state_data = None

    def reset(self):
        self.steps = 0
        self.total_cost = 0
        self.total_overflow = 0
        self.correct_actions = 0

        self.state_data = Observation(**self._generate_state())
        return self.state_data.dict()

    def state(self):
        return self.state_data.dict()

    def step(self, action: int):
        self.steps += 1

        state = self.state_data.dict()
        correct_bin = self._get_correct_bin(state["waste_type"])
        correct = (action == correct_bin)

        reward = 0.0

        # ===== EASY =====
        if self.task == "easy":
            reward = 1.0 if correct else 0.1

        # ===== MEDIUM =====
        elif self.task == "medium":
            reward = 0.6 if correct else 0.2
            reward -= state["contamination_level"] * 0.2

        # ===== HARD =====
        else:
            if correct:
                reward += 0.5

            reward -= state["overflow_risk"] * 0.3
            reward -= state["sorting_cost"] * 0.02

            # use truck arrival
            if state["truck_arrival"]:
                reward -= 0.1

        # normalize step reward
        reward = normalize_score(reward)

        # ===== TRACK =====
        if correct:
            self.correct_actions += 1

        self.total_cost += state["sorting_cost"]
        self.total_overflow += state["overflow_risk"]

        # ===== DONE =====
        done = self.steps >= self.max_steps

        if done:
            accuracy = self.correct_actions / self.steps
            efficiency = 1 - (self.total_cost / (self.steps * 10))
            safety = 1 - (self.total_overflow / self.steps)

            final_score = (0.5 * accuracy) + (0.3 * safety) + (0.2 * efficiency)

            # combine with last reward
            reward = normalize_score(reward + final_score)

        # next state
        self.state_data = Observation(**self._generate_state())

        return self.state_data.dict(), reward, done, {}

    def _generate_state(self):
        waste_types = ["plastic", "metal", "organic", "glass"]

        waste_type = random.choice(waste_types)

        # noise
        if random.random() < 0.2:
            waste_type = random.choice(waste_types)

        return {
            "waste_type": waste_type,
            "bin_capacity": [round(random.random(), 2) for _ in range(4)],
            "contamination_level": round(random.uniform(0, 1), 2),
            "time_pressure": random.randint(1, 100),

            "truck_arrival": random.choice([True, False]),
            "overflow_risk": round(random.uniform(0, 1), 2),
            "sorting_cost": random.randint(1, 10),
        }

    def _get_correct_bin(self, waste_type):
        mapping = {
            "plastic": 1,
            "metal": 2,
            "organic": 3,
            "glass": 4
        }
        return mapping.get(waste_type, 1)