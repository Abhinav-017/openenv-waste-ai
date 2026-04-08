from pydantic import BaseModel
from typing import List

class Observation(BaseModel):
    waste_type: str
    contamination_level: float
    bin_capacity: List[float]
    time_pressure: int

class Action(BaseModel):
    action: int

class Reward(BaseModel):
    value: float