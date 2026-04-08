import random
from .models import Observation

class WasteEnv:
    def __init__(self, level="easy"):
        self.level = level
        self.steps = 0
        self.state_data = None

    def reset(self):
        self.steps = 0
        self.state_data = Observation(**self._generate_state())
        return self.state()

    def state(self):
        return self.state_data.dict()

    def step(self, action):
        reward = self._calculate_reward(action)
        self.steps += 1

        done = self.steps >= 20

        self.state_data = Observation(**self._generate_state())

        return self.state(), reward, done, {}

    def _generate_state(self):
        waste_types = ["plastic", "organic", "metal", "glass"]

        if self.level == "easy":
            contamination = random.uniform(0, 0.2)
        elif self.level == "medium":
            contamination = random.uniform(0.2, 0.6)
        else:
            contamination = random.uniform(0.5, 1.0)

        return {
            "waste_type": random.choice(waste_types),
            "contamination_level": round(contamination, 2),
            "bin_capacity": [round(random.uniform(0, 1), 2) for _ in range(4)],
            "time_pressure": random.randint(0, 100)
        }

    def _calculate_reward(self, action):
        waste = self.state_data.waste_type
        contamination = self.state_data.contamination_level

        correct = {
            "organic": 2,
            "plastic": 1,
            "metal": 1,
            "glass": 1
        }

        if action == correct[waste]:
            return 1.0 if contamination < 0.3 else 0.5
        else:
            return -1.0