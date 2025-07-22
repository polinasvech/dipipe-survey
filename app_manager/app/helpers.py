import json
import random
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


def generate_random_hex_color():
    hex_chars = "0123456789ABCDEF"
    hex_color = "#"
    for _ in range(6):
        hex_color += random.choice(hex_chars)
    return hex_color
