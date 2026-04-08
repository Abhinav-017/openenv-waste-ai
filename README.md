# Waste Management RL Environment

## Motivation
This project simulates real-world waste sorting using reinforcement learning.

## Observation Space
- waste_type (str)
- contamination_level (float)
- bin_capacity (list)
- time_pressure (int)

## Action Space
0 landfill  
1 recycle  
2 compost  
3 reject  

## Tasks
- Easy: clean waste
- Medium: mixed contamination
- Hard: high contamination + pressure

## Reward Function
+1 correct  
+0.5 partial  
-1 incorrect  

## Setup
pip install -r requirements.txt

## Run
python inference.py

## Baseline Scores
Easy: ~0.8  
Medium: ~0.6  
Hard: ~0.4  