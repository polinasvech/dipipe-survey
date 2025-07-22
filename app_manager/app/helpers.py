import json
from typing import Dict


def load_json(filename: str) -> Dict:
    try:
        with open(f"data/{filename}", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: 'data.json' not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in 'data.json'.")
