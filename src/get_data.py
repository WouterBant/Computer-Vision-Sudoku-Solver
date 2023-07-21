from src.generate import generate_puzzle
import json
import os


# Check if the JSON file already exists
json_file = 'data/puzzles.json'
if os.path.exists(json_file):
    # Read existing puzzles from the file
    with open(json_file, 'r') as jsonfile:
        puzzles = json.load(jsonfile)
else:
    # If the file doesn't exist, start with an empty list
    puzzles = []

for _ in range(50000):
    solution, puzzle = generate_puzzle()
    puzzles.append({"puzzle": puzzle, "solution": solution})

# Save puzzles to JSON file
with open('data/puzzles.json', 'w') as jsonfile:
    json.dump(puzzles, jsonfile)
