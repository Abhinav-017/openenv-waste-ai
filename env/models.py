from pydantic import BaseModel
from typing import List

class Observation(BaseModel):
    waste_type: str
    bin_capacity: List[float]
    contamination_level: float
    time_pressure: int

    # advanced features
    truck_arrival: bool
    overflow_risk: float
    sorting_cost: int


class Action(BaseModel):
    action: int


class Reward(BaseModel):
    reward: float